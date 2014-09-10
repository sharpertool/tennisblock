
import validation
from validation import *

class KingBoardValidator(validation.BoardValidator):
    area = validation.AreaValidator(min_area=0.1,max_area=200)
    thickness = validation.ThicknessValidator(min=0.010,max=0.25)


class Board(object):

    def __init__(self,**kwargs):

        self._width = kwargs.get('width',0)
        self._height = kwargs.get('height',0)
        self._thickness = kwargs.get('thickness',0)

    def width(self):
        return self._width

    def height(self):
        return self._height

    def area(self):
        return self._width*self._height

    def thickness(self):
        return self._thickness

board = Board(width=20,height=40,thickness=0.067)

valid = KingBoardValidator()
if not valid.validate(board):
    print("Board is not valid!")
else:
    print("Board is valid!")

opts = {
    'area': globals()['AreaValidator'](min_area=0.1,max_area=900),
    'thickness' :validation.ThicknessValidator(min=0.010,max=0.25)
}
valid2 = type('MyBoardValidator',(validation.BoardValidator,),opts)()

if not valid2.validate(board):
    print("Board is not valid!")
else:
    print("Board is valid!")



