__author__ = 'sodabeta'

import sys
sys.path.append('../')
from lib.utils import _Type_Int,_Type_Float,_Type_Char,_Type_Boolean,gattrs

class ASTNode(object):
  def __init__(self):
    pass

  def codegen(self):
    pass

  def travle(self,indent=0):
    print self.dump(indent)
    attrs=gattrs(self)
    if isinstance(self,ListNode):
      for o in self.node_list:
        if isinstance(o,ASTNode):
          o.travle(indent+2)
    else:
      for o in attrs:
        v=getattr(self,o)
        if v and isinstance(v,ASTNode):
          v.travle(indent+2)      

  def dump(self, indent=0):
    return '{0}{1}'.format(
      ' ' * indent,self.__class__.__name__)

class ProgramNode(ASTNode):
  def __init__(self,phead,routine):
    self.head=phead
    self.routine=routine

  # def travle(self,indent=0):
  #   print self.dump(indent)
  #   self.head.travle(indent+2)
  #   self.routine.travle(indent+2)

class RoutineNode(ASTNode):
  def __init__(self,head,body):
    self.head=head    #RoutineHeadNode
    self.body=body    #

  # def travle(self,indent=0):
  #   print self.dump(indent)
  #   self.head.travle(indent+2)
  #   self.body.travle(indent+2)

class RoutineHeadNode(ASTNode):
  def __init__(self,const,typep,var,routine):
    self.const_part=const
    self.type_part=typep
    self.var_part=var
    self.routine_part=routine  

class RecordMemberNode(ASTNode):
  def __init__(self,var_name,field_name):
    self.var_name=var_name
    self.field_name=field_name

class ArrayMemberNode(ASTNode):
  def __init__(self,var_name,indices):
    self.var_name=var_name
    self.indices=indices



class ConstValueNode(ASTNode):
  def __init__(self,type,cvalue):
    self.type=type              #string
    self.value=cvalue           #if type=='int' then int else string

class TypeDefinitionNode(ASTNode):
  def __init__(self,name,type_decl):
    self.name=name              #string
    self.type=type_decl         #TypeNode

class TypeNode(ASTNode):
  pass

class SimpleTypeNode(TypeNode):
  def __init__(self,type_name,detail=None):
    self.type_name=type_name      #string    
    self.detail=detail

class EnumTypeNode(TypeNode):
  def __init__(self,enum_name_list):
    self.name_list=enum_name_list #NameListNode

class RangeTypeNode(TypeNode):
  def __init__(self,lb,rb):
    self.lb=lb                  #ConstValueNode
    self.rb=rb                  #ConstValueNode

class VariableTypeNode(TypeNode):
  def __init__(self,typename):
    self.typename=typename

class ArrayTypeNode(TypeNode):
  def __init__(self,bound,type_name):
    assert(isinstance(bound,RangeTypeNode),'The bound should be RangeTypeNode type')
    self.bound=bound              #should be RangeTypeNode
    self.type_name=type_name      #TypeNode

class RecordTypeNode(TypeNode):
  def __init__(self,field_decl_list):
    self.field_decl_list=field_decl_list #FieldDeclListNode  

class ParaTypeListNode(ASTNode):
  def __init__(self,var_list,type):
    self.var_list=var_list
    self.type=type
  
class VarDeclNode(ASTNode):
  def __init__(self,name_list,typenode):
    self.name_list=name_list            #NameListNode
    self.type=typenode                  #TypeNode

class FunctionDeclNode(ASTNode):
  def __init__(self,prototype,body):
    self.prototype=prototype
    self.body=body

class FunctionPrototypeNode(ASTNode):
  def __init__(self,fn_name,params,return_type):
    self.name=fn_name
    self.params=params
    self.return_type=return_type

class ProcedureDeclNode(ASTNode):
  def __init__(self,prototype,body):
    self.prototype=prototype
    self.body=body

class ProcedurePrototypeNode(ASTNode):
  def __init__(self,fn_name,params):
    self.name=fn_name
    self.params=params



######################## List Node ############################

class ListNode(ASTNode):
  def __init__(self,node=None):
    self.node_list=[]
    if node is not None:
      self.node_list.append(node)

  def append(self,node):
    self.node_list.append(node)

class ConstExprListNode(ListNode):
  pass

class TypeDeclListNode(ListNode):
  pass

class StmtListNode(ListNode):
  pass
  
class FieldDeclListNode(ListNode):
  pass

class NameListNode(ListNode):
  pass

class VarDeclListNode(ListNode):
  pass

class CaseExprListNode(ListNode):
  pass

class ExprList(ListNode):
  pass

class FunctionDeclListNode(ListNode):
  pass

class ProcedureDeclListNode(ListNode):
  pass

class ParaDeclListNode(ListNode):
  pass

class FunctionArgsListNode(ListNode):
  pass

##################################################################

# VariableNode
# RecordMemberNode
# ArrayMemberNode
# ConstValueNode
# ConstExprNode

class ExprNode(ASTNode):
  def __init__(self):
    self.type=_Type_Int

  def parse_type(self,type_name):
    if t in ('int','integer'):
      return _Type_Int
    elif t in ('real'):
      return _Type_Float
    elif t in ('char'):
      return _Type_Char
    elif t in ('boolean'):
      return _Type_Boolean
    else:
      raise Exception('invalid type name')

class ConstExprNode(ExprNode):
  def __init__(self,var,cvalue):
    super(self.__class__,self).__init__()
    self.var=var                #VariableNode
    self.const_value=cvalue     #ConstValueNode
    self.type=self.parse_type(self.const_value.type)

class VariableNode(ExprNode):
  def __init__(self,id_name):
    super(self.__class__,self).__init__()
    self.name=id_name

class BinaryExpr(ExprNode):
  def __init__(self,op,lhs,rhs):
    self.op=op
    self.lhs=lhs
    self.rhs=rhs

class UnaryExpr(ExprNode):
  def __init__(self,op,expr):
    self.op=op
    self.expr=expr

class CallExpr(ExprNode):
  def __init__(self,callee,args):
    self.callee=callee
    self.args=args

class IfExpr(ExprNode):
  def __init__(self,cond_expr,then_expr,else_expr):
    self.cond_expr=cond_expr
    self.then_expr=then_expr
    self.else_expr=else_expr

class RepExpr(ExprNode):
  def __init__(self,cond_expr,body):
    self.cond_expr=cond_expr
    self.body=body

class WhileExpr(ExprNode):
  def __init__(self,cond_expr,body):
    self.cond_expr=cond_expr
    self.body=body

class ForExpr(ExprNode):
  def __init__(self,id_name,start_expr,direction,end_expr,body):
    self.id_name=id_name
    self.start_expr=start_expr
    self.end_expr=end_expr
    self.dir=direction
    self.body=body

class CaseStmtExpr(ExprNode):
  def __init__(self,expr,case_expr_list):
    self.expr=expr
    self.case_expr_list=case_expr_list

class CaseExpr(ExprNode):
  def __init__(self,value,action):
    self.value=value
    self.action=action

class SysFunctionNode(ASTNode):
  def __init__(self,name,args=None):
    self.name=name
    self.args=args
    
# = fn if rep while for case_stmt case_expr goto bin_expr sin_expr
def create_stmt_node(*p):
  op=p[0]
  if op == ':=':
    return BinaryExpr(':=',p[1],p[2])
  elif op == 'fn':
    return CallExpr(p[1],p[2])
  elif op == 'if':
    return IfExpr(p[1],p[2],p[3])
  elif op == 'rep':
    return RepExpr(p[2],p[1])
  elif op == 'while':
    return WhileExpr(p[1],p[2])
  elif op == 'for':
    return ForExpr(p[1],p[2],p[3],p[4],p[5])
  elif op == 'case_stmt':
    return CaseStmtExpr(p[1],p[2])
  elif op == 'case_expr':
    return CaseExpr(p[1],p[2])
  elif op == 'goto':
    return None
  elif op == 'bin_expr':
    return BinaryExpr(p[1],p[2],p[3])
  elif op == 'sin_expr':
    return UnaryExpr(p[1],p[2])
  else:
    assert(False,'Invalid keyword in create_stmt_node')