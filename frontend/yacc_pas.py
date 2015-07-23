__author__ = 'sodabeta'

import sys
import ply.yacc as yacc
from lex_pas import tokens

sys.path.append('./')
from AST import *

precedence=(
  ('left','oPLUS','oMINUS'),
  ('left','oMUL','oDIV','kDIV','kMOD')
)

error_list=[]

def p_Start(p):
  'program : program_head routine oDOT'
  p[0]=ProgramNode(p[1],p[2])

def p_Program_head(p):
  'program_head : kPROGRAM yNAME oSEMI'  
  p[0]=p[2]

def p_Routine(p):
  'routine : routine_head routine_body'
  p[0]=RoutineNode(p[1],p[2])

def p_Routine_head(p):
  'routine_head : const_part type_part var_part routine_part'
  p[0]=RoutineHeadNode(p[1],p[2],p[3],p[4])  


# const_part : CONST  const_expr_list  |  empty
def p_Const_part(p):
  '''const_part : kCONST  const_expr_list
                | empty'''
  if len(p)==3:
    p[0]=p[2]
  else:
    p[0]=None

# const_expr_list : const_expr_list  ID  EQUAL  const_value  SEMI | ID  EQUAL  const_value  SEMI
def p_Const_expr_list_1(p):
  'const_expr_list : const_expr_list yNAME oEQUAL const_value oSEMI'
  e=ConstExprNode(VariableNode(p[2]),p[4])
  p[0]=p[1]
  p[0].append(e)

def p_Const_expr_list_2(p):
  'const_expr_list : yNAME oEQUAL const_value oSEMI'
  e=ConstExprNode(p[1],p[3])
  p[0]=ConstExprListNode(e)


# const_value : INTEGER  |  REAL  |  CHAR  |  STRING  |  SYS_CON
def p_Const_value_1(p):
  'const_value : cINTEGER'
  p[0]=ConstValueNode('int',p[1])

def p_Const_value_2(p):
  'const_value : cREAL'
  p[0]=ConstValueNode('real',p[1])

def p_Const_value_3(p):
  'const_value : cCHAR'
  p[0]=ConstValueNode('char',p[1])

def p_Const_value_4(p):
  'const_value : cSTRING'
  p[0]=ConstValueNode('str',p[1])

def p_Const_value_5(p):
  'const_value : cSYS_CON'
  p[0]=ConstValueNode('syscon',p[1])

# type_part : TYPE type_decl_list  |  empty
def p_Type_part(p):
  '''type_part : kTYPE type_decl_list
               | empty'''
  if len(p)==3:
    p[0]=p[2]
  else:
    p[0]=None

# type_decl_list : type_decl_list  type_definition  |  type_definition
def p_Type_decl_list_1(p):
  'type_decl_list : type_decl_list  type_definition'
  p[0]=p[1]
  p[0].append(p[2])

def p_Type_decl_list_2(p):
  'type_decl_list : type_definition'
  p[0]=TypeDeclListNode(p[1])

# type_definition : ID  EQUAL  type_decl  SEMI
def p_Type_definition(p):
  'type_definition : yNAME oEQUAL type_decl oSEMI'
  p[0]=TypeDefinitionNode(p[1],p[3])

# type_decl : simple_type_decl  |  array_type_decl  |  record_type_decl
def p_Type_decl(p):
  '''type_decl : simple_type_decl
               | array_type_decl
               | record_type_decl'''
  p[0]=p[1]


# simple_type_decl : SYS_TYPE  |  ID  |  LP  name_list  RP  
                # |  const_value  DOTDOT  const_value
                # |  MINUS  const_value  DOTDOT  const_value
                # |  MINUS  const_value  DOTDOT  MINUS  const_value
                # |  ID  DOTDOT  ID
def p_Simple_type_decl_1(p):
  'simple_type_decl : cSYS_TYPE'
  p[0]=SimpleTypeNode(p[1])

def p_Simple_type_decl_2(p):
  'simple_type_decl : oLP name_list oRP'
  p[0]=EnumTypeNode('enum',p[2])

def p_Simple_type_decl_3(p):
  'simple_type_decl : const_value oDOTDOT const_value'
  p[0]=RangeTypeNode('range',(p[1],p[3]))

def p_Simple_type_decl_4(p):
  'simple_type_decl : yNAME'
  p[0]=VariableTypeNode(p[1])

# array_type_decl : ARRAY  LB  simple_type_decl  RB  OF  type_decl
def p_Array_type_decl(p):
  'array_type_decl : kARRAY  oLB  simple_type_decl  oRB  kOF  type_decl'
  p[0]=ArrayTypeNode(p[3],p[6])


# record_type_decl : RECORD  field_decl_list  END
def p_Record_type_decl(p):
  'record_type_decl : kRECORD  field_decl_list  kEND'
  p[0]=RecordTypeNode(p[2]);

# field_decl_list : field_decl_list  field_decl  |  field_decl
def p_Field_decl_list_1(p):
  'field_decl_list : field_decl_list  field_decl'
  p[0]=p[1]
  p[0].append(p[2])

def p_Field_decl_list_2(p):
  'field_decl_list : field_decl'
  p[0]=FieldDeclListNode(p[1])

# field_decl : name_list  COLON  type_decl  SEMI
def p_Field_decl(p):
  'field_decl : name_list  oCOLON  type_decl  oSEMI'
  pass

# name_list : name_list  COMMA  ID  |  ID
def p_Name_list_1(p):
  'name_list : name_list  oCOMMA  yNAME'
  p[0]=p[1]
  p[0].append(p[3])

def p_Name_list_2(p):
  'name_list : yNAME'
  p[0]=NameListNode(p[1])

# var_part : VAR  var_decl_list  |  empty
def p_Var_part(p):
  '''var_part : kVAR  var_decl_list
              | empty'''
  if len(p)==3:
    p[0]=p[2]
  else:
    p[0]=None

# var_decl_list :  var_decl_list  var_decl  |  var_decl
def p_Var_decl_list_1(p):
  'var_decl_list :  var_decl_list  var_decl'
  p[0]=p[1]
  p[0].append(p[2])

def p_Var_decl_list_2(p):
  'var_decl_list : var_decl'
  p[0]=VarDeclListNode(p[1])

# var_decl :  name_list  COLON  type_decl  SEMI
def p_Var_decl(p):
  'var_decl :  name_list  oCOLON  type_decl  oSEMI'
  p[0]=VarDeclNode(p[1],p[3])


# routine_part :  routine_part  function_decl  |  routine_part  procedure_decl
#            | function_decl  |  procedure_decl  | empty

def p_Routine_part_1(p):
  'routine_part :  routine_part  function_decl'
  p[0]=p[1]
  p[0].append(p[2])

def p_Routine_part_2(p):
  'routine_part :  function_decl'
  p[0]=FunctionDeclListNode(p[1])

def p_Routine_part_3(p):
  'routine_part :  routine_part  procedure_decl'
  p[0]=p[1]
  p[0].append(p[2])

def p_Routine_part_4(p):
  'routine_part :  procedure_decl'
  p[0]=ProcedureDeclListNode(p[1])

def p_Routine_part_5(p):
  'routine_part : empty'
  p[0]=None

# function_decl : function_head  SEMI  sub_routine  SEMI
def p_Function_decl(p):
  'function_decl : function_head  oSEMI  sub_routine oSEMI'
  p[0]=FunctionDeclNode(p[1],p[3])

# function_head :  FUNCTION  ID  parameters  COLON  simple_type_decl 
def p_Function_head(p):
  'function_head :  kFUNCTION  yNAME  parameters  oCOLON  simple_type_decl '
  p[0]=FunctionPrototypeNode(p[2],p[3],p[5])

# procedure_decl :  procedure_head  SEMI  sub_routine  SEMI
def p_Prodecure_decl(p):
  'procedure_decl :  procedure_head  oSEMI  sub_routine  oSEMI'
  p[0]=ProcedureDeclNode(p[1],p[3]);

# sub_routine : routine
def p_Sub_routine(p):
  'sub_routine : routine'
  p[0]=p[1]

# procedure_head :  PROCEDURE ID parameters 
def p_Procedure_head(p):
  'procedure_head :  kPROCEDURE yNAME parameters'
  p[0]=ProcedurePrototypeNode(p[2],p[3]);

# parameters : LP  para_decl_list  RP  |  empty
def p_Parameters(p):
  '''parameters : oLP  para_decl_list  oRP
                | empty'''
  if len(p)==2:
    p[0]=None
  else:
    p[0]=p[2]

# para_decl_list : para_decl_list  SEMI  para_type_list  |  para_type_list
def p_Para_decl_list_1(p):
  'para_decl_list : para_decl_list  oSEMI  para_type_list'
  p[0]=p[1]
  p[0].append(p[3])

def p_Para_decl_list_2(p):
  'para_decl_list : para_type_list'
  p[0]=ParaDeclListNode(p[1])

# para_type_list : var_para_list COLON  simpe_type_decl  |  val_para_list  COLON  simple_type_decl
def p_Para_type_list_2(p):
  'para_type_list : var_para_list  oCOLON  simple_type_decl'
  p[0]=ParaTypeListNode(p[1],p[3])

# var_para_list : VAR  name_list
def p_Var_para_list_1(p):
  'var_para_list : kVAR  name_list'
  p[0]=p[2]

# val_para_list : name_list
def p_Var_para_list_2(p):
  'var_para_list : name_list'
  p[0]=p[1]

def p_Routine_body(p):
  'routine_body : compound_stmt'
  p[0]=p[1]

def p_Stmt_list(p):
  '''stmt_list : stmt_list stmt oSEMI
               | empty'''
  if(len(p)==4):
    if p[1] is None:      
      p[0]=StmtListNode(p[2])
    else:
      p[0]=p[1]
      p[0].append(p[2])
  else:
    p[0]=None

def p_Stmt_list_error(p):
  'stmt_list : stmt_list stmt error'  
  process_syntax_error(p,3,';')
  p[0]=None

def p_Stmt(p):
  '''stmt : cINTEGER  oCOLON  non_label_stmt
          | non_label_stmt'''
  if len(p)==4:
    p[3].set_id(p[1])
    p[0]=p[3]
  else:
    p[0]=p[1]

def p_Non_label_stmt(p):
  '''non_label_stmt : assign_stmt
                    | proc_stmt
                    | compound_stmt
                    | if_stmt
                    | repeat_stmt
                    | while_stmt
                    | for_stmt
                    | case_stmt
                    | goto_stmt'''
  p[0]=p[1]

# assign_stmt : ID  ASSIGN  expression
#            | ID LB expression RB ASSIGN expression
#            | ID  DOT  ID  ASSIGN  expression

def p_Assign_stmt_1(p):
  'assign_stmt : yNAME  oASSIGN  expression'
  # print '$$$$$ ',p.lineno(1),p.lexpos(1)
  var=VariableNode(p[1])
  p[0]=create_stmt_node(':=',var,p[3])

def find_column(pos):
  print parser.text

def process_syntax_error(p,error_pos,expected_token):
  global error_list  
  # print 'syntax error in line %d at %d'%(p.lineno(error_pos),find_column(p.lexpos(2)))
  error_list.append((p.lineno(error_pos),p.lexpos(2),expected_token,p[error_pos].value))
  # print '@@@@@@@@@'
  # print p[error_pos].value

def p_Assign_stmt_1_error(p):
  'assign_stmt : yNAME  error  expression'  
  process_syntax_error(p,2,':=')  
  p[0]=None

def p_Assign_stmt_2(p):
  'assign_stmt : yNAME oLB expression oRB oASSIGN expression'
  var=ArrayMemberNode(p[1],[p[3]])
  p[0]=create_stmt_node(':=',var,p[6])

def p_Assign_stmt_3(p):
  'assign_stmt : yNAME  oDOT yNAME oASSIGN  expression'
  var=RecordMemberNode(p[1],p[3])
  p[0]=create_stmt_node(':=',var,p[5])

# proc_stmt : ID
#           |  ID  LP  args_list  RP
#           |  SYS_PROC
#           |  SYS_PROC  LP  expression_list  RP
#           |  READ  LP  factor  RP

def p_Proc_stmt_1(p):
  'proc_stmt : yNAME'
  # p[0]=create_stmt_node('fn',p[1].name)
  p[0]=VariableNode(p[1])

def p_Proc_stmt_2(p):
  'proc_stmt : yNAME oLP args_list oRP'
  p[0]=create_stmt_node('fn',p[1],p[3])

#to implement system functions
def p_Proc_stmt_3(p):
  'proc_stmt : SYS_PROC'
  p[0]=p[1]

def p_Proc_stmt_4(p):
  'proc_stmt : SYS_PROC oLP expression_list oRP'
  p[0]=create_stmt_node('fn',p[1],p[3])

def p_Proc_stmt_5(p):
  'proc_stmt : kREAD oLP factor oRP'
  p[0]=create_stmt_node('fn',p[1],p[3])

# def p_Proc_stmt_6(p):
#   'proc_stmt : kREADLN oLP factor oRP'
#   p[0]=create_stmt_node('fn',p[1],p[3])

# compound_stmt : BEGIN  stmt_list  END | empty

def p_Compound_stmt(p):
  '''compound_stmt : kBEGIN stmt_list kEND
                   | empty'''
  if len(p)==4:
    p[0]=p[2]
  else:
    p[0]=None

# if_stmt : IF  expression  THEN  stmt  else_clause

def p_If_stmt(p):
  'if_stmt : kIF expression kTHEN stmt else_clause'
  p[0]=create_stmt_node('if',p[2],p[4],p[5])

# else_clause : ELSE stmt | empty

def p_Else_clause(p):
  '''else_clause : kELSE stmt
                 | empty'''
  if len(p)==3:
    p[0]=p[2]
  else:
    p[0]=None

# repeat_stmt : REPEAT  stmt_list  UNTIL  expression

def p_Repeat_stmt(p):
  'repeat_stmt : kREPEAT stmt_list kUNTIL expression'
  p[0]=create_stmt_node('rep',p[2],p[4])

# while_stmt : WHILE  expression  DO stmt
def p_While_stmt(p):
  'while_stmt : kWHILE  expression  kDO stmt'
  p[0]=create_stmt_node('while',p[2],p[4])

# for_stmt : FOR  ID  ASSIGN  expression  direction  expression  DO stmt
def p_For_stmt(p):
  'for_stmt : kFOR  yNAME  oASSIGN  expression  direction  expression  kDO stmt'  
  pdir=ConstValueNode('int',p[5].value)
  # print pdir.value,p[5].value
  p[0]=create_stmt_node('for',p[2],p[4],pdir,p[6],p[8])

# direction : TO | DOWNTO
def p_Direction(p):
  '''direction : kTO
               | kDOWNTO'''
  # print 'p[1]=',p[1]
  p[0]=1 if p[1] == 'to' else -1
  p[0]=ConstValueNode('int',p[0])

# case_stmt : CASE expression OF case_expr_list  END
def p_Case_stmt(p):
  'case_stmt : kCASE expression kOF case_expr_list  kEND'
  p[0]=create_stmt_node('case_stmt',p[2],p[4])

# case_expr_list : case_expr_list  case_expr  |  case_expr
def p_Case_expr_list(p):
  '''case_expr_list : case_expr_list  case_expr
                    | case_expr'''
  if len(p)==3:
    if p[1] is None:
      p[0]=p[2]
    else:
      p[1].append(p[2])
      p[0]=p[1]
  else:
    p[0]=CaseExprListNode(p[1])
    # p[0]=p[1]


# case_expr : const_value  COLON  stmt  SEMI
#           |  ID  COLON  stmt  SEMI
def p_Case_expr(p):
  '''case_expr : const_value  oCOLON  stmt  oSEMI
               | yNAME  oCOLON  stmt  oSEMI'''
  p[0]=create_stmt_node('case_expr',p[1],p[3])


# goto_stmt : GOTO  INTEGER
def p_Goto_stmt(p):
  'goto_stmt : kGOTO  cINTEGER'
  p[0]=create_stmt_node('goto',p[2])

# expression_list : expression_list  COMMA  expression  |  expression
def p_Expression_list(p):
  '''expression_list : expression_list  oCOMMA  expression
                     | expression'''
  if len(p)==4:
    if p[3] is not None:
      p[1].append(p[3])
      p[0]=p[1]
    else:
      p[0]=p[1]
  else:
    p[0]=ExprList(p[1])
    # p[0]=p[1]

# expression : expression  GE  expr  |  expression  GT  expr  |  expression  LE  expr
#           |  expression  LT  expr  |  expression  EQUAL  expr  
#           |  expr
def p_Expression_1(p):
  '''expression : expression  oGE  expr
                | expression  oGT  expr
                | expression  oLE  expr
                | expression  oLT  expr
                | expression  oEQUAL  expr'''
  p[0]=create_stmt_node('bin_expr',p[2],p[1],p[3])

def p_Expression_2(p):
  'expression : expr'
  p[0]=p[1]

# expr : expr  PLUS  term  |  expr  MINUS  term  |  expr  OR  term  |  term
def p_Expr(p):
  '''expr : expr  oPLUS  term
          | expr  oMINUS  term
          | expr  kOR  term
          | term'''
  if len(p)==4:
    p[0]=create_stmt_node('bin_expr',p[2],p[1],p[3])
  else:
    p[0]=p[1]


# term : term  MUL  factor  |  term  DIV  factor  |  term  MOD  factor 
#  |  term  AND  factor  |  factor
def p_Term(p):
  '''term : term  oMUL  factor
          | term  kDIV  factor
          | term  kMOD  factor 
          | term  kAND  factor
          | factor'''
  if len(p)==4:
    p[0]=create_stmt_node('bin_expr',p[2],p[1],p[3])
  else:
    p[0]=p[1]


# factor : ID  |  ID  LP  args_list  RP  |  SYS_FUNCT  |  
#          SYS_FUNCT  LP  args_list  RP  |  const_value  |  LP  expression  RP
#         |  NOT  factor  |  MINUS  factor  |  ID  LB  expression  RB
#         |  ID  DOT  ID
def p_Factor_1(p):
  'factor : yNAME'
  p[0]=VariableNode(p[1])

def p_Factor_2(p):
  'factor : yNAME  oLB  expression  oRB'
  p[0]=ArrayMemberNode(p[1],[p[3]])  

def p_Factor_3(p):
  'factor : const_value'
  p[0]=p[1]

def p_Factor_4(p):
  'factor : oLP  expression  oRP'
  p[0]=p[2]

def p_Factor_5(p):
  '''factor : kNOT factor
            | oMINUS factor'''
  p[0]=create_stmt_node('sin_expr',p[1],p[2])

def p_Factor_6(p):
  'factor : yNAME oDOT yNAME'
  p[0]=RecordMemberNode(p[1],p[3])

def p_Factor_7(p):
  'factor : yNAME oLP args_list oRP'
  p[0]=create_stmt_node('fn',p[1],p[3])

def p_Factor_8(p):
  'factor : SYS_FUNCT'
  p[0]=create_stmt_node('fn',p[1],None)

def p_Factor_9(p):
  'factor : SYS_FUNCT oLP args_list oRP'  
  p[0]=create_stmt_node('fn',p[1],p[3])

# args_list : args_list  COMMA  expression  |  expression
def p_Args_list(p):
  '''args_list : args_list  oCOMMA  expression
               | expression'''
  if len(p)==4:
    p[0]=p[1]
    p[0].append(p[3])
  else:
    p[0]=FunctionArgsListNode(p[1])


# const_value : INTEGER  |  REAL  |  CHAR  |  STRING  |  SYS_CON
# def p_error(p):
#   print 'p ',p
#   if p:
#     print 'Syntax error at token',p.type
#     parser.errok()
#   else:
#     print 'ERROR!'

def p_empty(p):
  'empty :'  

# import logging
# logging.basicConfig(
#   level = logging.DEBUG,
#   filename = "parselog_yacc.txt",
#   filemode = "w", 
#   format = "%(filename)10s:%(lineno)4d:%(message)s"
# )
# log=logging.getLogger()
from lex_pas import log
parser=yacc.yacc(debug=True,debuglog=log)