from __future__ import print_function
from ortools.sat.python import cp_model

def solve(cells):
  sub_block_mask = (
    (0, 0, 0, 1, 1, 1, 2, 2, 2),
    (0, 0, 0, 1, 1, 1, 2, 2, 2),
    (0, 0, 0, 1, 1, 1, 2, 2, 2),
    (3, 3, 3, 4, 4, 4, 5, 5, 5),
    (3, 3, 3, 4, 4, 4, 5, 5, 5),
    (3, 3, 3, 4, 4, 4, 5, 5, 5),
    (6, 6, 6, 7, 7, 7, 8, 8, 8),
    (6, 6, 6, 7, 7, 7, 8, 8, 8),
    (6, 6, 6, 7, 7, 7, 8, 8, 8),
  )
  model = cp_model.CpModel()

  # 9x9=81このセルを変数で表現する。
  # すでに値がセットされている値はその値のみ、そうでない場合は１から9までのいずれかの値をとる。
  variables = [ [ model.NewIntVar(1, 9, f'cell{x}{y}') if array[y][x] == 0 else model.NewIntVar(array[y][x], array[y][x], f'cell{x}{y}') for x in range(9)] for y in range(9)]

  # 制約を設定する。
  # 横１行で数値の重複ができないことの制約を追加
  for y in range(9):
    model.AddAllDifferent(variables[y])
  # 縦１列で数値の重複ができないことの制約を追加
  for x in range(9):
    model.AddAllDifferent([ variables[y][x] for y in range(9) ])
  # sub_block_mask で同じ値のセル同士は数値の重複が出来ないことの制約を追加
  for s in range(9):
    model.AddAllDifferent([ variables[y][x] for x in range(9) for y in range(9) if sub_block_mask[y][x] == s ])

  # ソルバーを生成して、上記の制約を満たす解を求める。
  solver = cp_model.CpSolver()
  status = solver.Solve(model)
  if status == cp_model.FEASIBLE:
    return [ [ solver.Value(variables[y][x]) for x in range(9) ] for y in range(9) ]
  else:
    return []


if __name__ == '__main__':

  # スパコンで力任せに作った数独の難問
  # http://apollon.issp.u-tokyo.ac.jp/~watanabe/sample/sudoku/index_j.html#intro
  # array = (
  #     (0, 8, 0, 0, 0, 0, 1, 5, 0,),
  #     (4, 0, 6, 5, 0, 9, 0, 8, 0,),
  #     (0, 0, 0, 0, 0, 8, 0, 0, 0,),
  #     (0, 0, 0, 0, 0, 0, 0, 0, 0,),
  #     (0, 0, 2, 0, 4, 0, 0, 0, 3,),
  #     (3, 0, 0, 8, 0, 1, 0, 0, 0,),
  #     (9, 0, 0, 0, 7, 0, 0, 0, 0,),
  #     (6, 0, 0, 0, 0, 0, 0, 0, 4,),
  #     (1, 5, 0, 0, 0, 0, 0, 9, 0,),
  # )
  # フィンランドの数学者、 Dr. Arto Inkala氏によるもの
  # http://www.aisudoku.com/index_en.html
  array = (
      (8, 0, 0, 0, 0, 0, 0, 0, 0,),
      (0, 0, 3, 6, 0, 0, 0, 0, 0,),
      (0, 7, 0, 0, 9, 0, 2, 0, 0,),
      (0, 5, 0, 0, 0, 7, 0, 0, 0,),
      (0, 0, 0, 0, 4, 5, 7, 0, 0,),
      (0, 0, 0, 1, 0, 0, 0, 3, 0,),
      (0, 0, 1, 0, 0, 0, 0, 6, 8,),
      (0, 0, 8, 5, 0, 0, 0, 1, 0,),
      (0, 9, 0, 0, 0, 0, 4, 0, 0,),
  )

  ans = solve(array)

  for rows in ans:
    print("".join(map(str, rows)))
