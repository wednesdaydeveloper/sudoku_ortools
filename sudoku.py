from __future__ import print_function
from ortools.sat.python import cp_model
import math

def solve(cells):
  size = 16
  rsize = int(math.sqrt(size))

  sub_block_mask = tuple(tuple(int(i/rsize) + int(j/rsize)*rsize for i in range(size)) for j in range(size))

  model = cp_model.CpModel()
  # size の2乗個のセルを変数で表現する。
  # すでに値がセットされている値はその値のみ、そうでない場合は１から size までのいずれかの値をとる。
  variables = [ [ model.NewIntVar(1, size, f'cell{x}{y}') if array[y][x] == 0 else model.NewIntVar(array[y][x], array[y][x], f'cell{x}{y}') for x in range(size)] for y in range(size)]

  # 制約を設定する。
  # 横１行で数値の重複ができないことの制約を追加
  for y in range(size):
    model.AddAllDifferent(variables[y])
  # 縦１列で数値の重複ができないことの制約を追加
  for x in range(size):
    model.AddAllDifferent([ variables[y][x] for y in range(size) ])
  # sub_block_mask で同じ値のセル同士は数値の重複が出来ないことの制約を追加
  for s in range(size):
    model.AddAllDifferent([ variables[y][x] for x in range(size) for y in range(size) if sub_block_mask[y][x] == s ])

  # ソルバーを生成して、上記の制約を満たす解を求める。
  solver = cp_model.CpSolver()
  status = solver.Solve(model)
  if status == cp_model.FEASIBLE:
    return [ [ solver.Value(variables[y][x]) for x in range(size) ] for y in range(size) ]
  else:
    return []
  
if __name__ == '__main__':
  array = (
    ( 0, 0, 2,15, 0, 0, 0, 0,11, 0,10, 0, 0, 3, 0, 0),
    ( 5,11, 0, 0,13, 0,15, 0, 0,14, 0, 0, 0,12,10, 0),
    (15, 0, 0, 0, 0, 1,11, 0, 2, 0,13, 0,15, 0, 7, 0),
    ( 0,12,13, 0, 3, 7, 0, 2, 0, 5, 0,15, 0, 0,11, 0),
    ( 0, 0, 0,11, 5, 0, 0, 0,10, 0, 8, 0, 0, 0, 4, 7),
    (13, 0,12, 0, 0, 8, 0,15, 0, 0, 0, 2, 9,11, 0, 0),
    ( 0, 5, 0,15, 0, 0, 7,13, 0, 3, 0,11, 0, 0, 2, 8),
    ( 2, 0, 7, 0, 4, 0, 0,11,15, 0, 5, 6,10, 0, 0, 0),
    (11, 0, 8, 0, 2, 0, 0, 6, 5, 0,15, 9,12, 0, 0, 0),
    ( 0, 2, 0, 5, 0, 0,13, 7, 0,10, 0, 1, 0, 0, 8, 3),
    ( 1, 0,15, 0, 0,10, 0, 5, 0, 0, 0,12, 2,13, 0, 0),
    ( 0, 0, 0, 9,15, 0, 0, 0, 4, 0,11, 0, 0, 0, 5,15),
    ( 0,13, 4, 0, 7, 2, 0,14, 0,11, 0, 8, 0, 0,15, 0),
    ( 3, 0, 0, 0, 0,15, 4, 0,13, 0, 2, 0, 7, 0, 6, 0),
    ( 7,15, 0, 0,11, 0, 5, 0, 0, 1, 0, 0, 0, 2,14, 0),
    ( 0, 0, 5, 2, 0, 0, 0, 0, 6, 0, 7, 0, 0,15, 0, 0),
  )
  
  ## スパコンで力任せに作った数独の難問
  ## http://apollon.issp.u-tokyo.ac.jp/~watanabe/sample/sudoku/index_j.html#intro
  #array = (
  #    (0, 8, 0, 0, 0, 0, 1, 5, 0,),
  #    (4, 0, 6, 5, 0, 9, 0, 8, 0,),
  #    (0, 0, 0, 0, 0, 8, 0, 0, 0,),
  #    (0, 0, 0, 0, 0, 0, 0, 0, 0,),
  #    (0, 0, 2, 0, 4, 0, 0, 0, 3,),
  #    (3, 0, 0, 8, 0, 1, 0, 0, 0,),
  #    (9, 0, 0, 0, 7, 0, 0, 0, 0,),
  #    (6, 0, 0, 0, 0, 0, 0, 0, 4,),
  #    (1, 5, 0, 0, 0, 0, 0, 9, 0,),
  #)
  # フィンランドの数学者、 Dr. Arto Inkala氏によるもの
  # http://www.aisudoku.com/index_en.html
#   array = (
#       (8, 0, 0, 0, 0, 0, 0, 0, 0,),
#       (0, 0, 3, 6, 0, 0, 0, 0, 0,),
#       (0, 7, 0, 0, 9, 0, 2, 0, 0,),
#       (0, 5, 0, 0, 0, 7, 0, 0, 0,),
#       (0, 0, 0, 0, 4, 5, 7, 0, 0,),
#       (0, 0, 0, 1, 0, 0, 0, 3, 0,),
#       (0, 0, 1, 0, 0, 0, 0, 6, 8,),
#       (0, 0, 8, 5, 0, 0, 0, 1, 0,),
#       (0, 9, 0, 0, 0, 0, 4, 0, 0,),
#   )
  start = time.time()
  ans = solve(array)
  elapsed_time = time.time() - start
  print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
  print ('\n'.join(textwrap.wrap(array2string(ans), 9)))
