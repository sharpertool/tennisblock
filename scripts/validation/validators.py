class Validator(object):

    # Tracks each time a Field instance is created. Used to retain order.
    creation_counter = 0

    def validate(self,board):
        return True


class AreaValidator(Validator):
    MAX_AREA = 100

    def __init__(self,min_area=None,max_area=None):
        super(AreaValidator,self).__init__()

        if not min_area or not max_area:
            raise Exception("Must specify a min and maximum thickness.")

        self.min_area = min_area
        self.max_area = max_area

    def validate(self,board):
        """
        Insure the size of the board is within manufacturer
        specifications
        """
        area = board.width() * board.height()
        if self.min_area < area < self.max_area:
            return True
        return False

class ThicknessValidator(Validator):

    def __init__(self,min=None,max=None):
        super(ThicknessValidator,self).__init__()

        if not min or not max:
            raise Exception("Must specify a min and maximum thickness.")
        self.min = min
        self.max = max

    def validate(self,board):
        """
        Insure the thickness of the board
        specifications
        """
        if self.min < board.thickness() < self.max:
            return True

        return False



