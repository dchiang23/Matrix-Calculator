"""
Sources:
1. https://www.w3schools.com/python/python_strings_slicing.asp
2. https://www.w3schools.com/python/ref_string_join.asp


"""

class Matrix:
    __slots__ = ("_num_rows", "_num_cols", "_data")

    def _directData(self, num_rows: int, num_cols: int, data: list[int])->None:
        """
        Args:
            num_rows (int): number of rows in the matrix
            num_cols (int): number of columns in the matrix
            data (list[int]): the numbers in the matrix
        """
        #check format
        hypoSize = num_rows*num_cols
        if hypoSize != len(data):
            raise ValueError("Dimension does not match the amount of data given")
        else:
            #use data to define instance variables i.e helper function 1
            self._num_rows = num_rows
            self._num_cols = num_cols
            self._data = data
          
    def _readFile(self, filename: str)->None:
        """
        Args:
            filename (str): this is matrix that the user wants to evalulate in file form
        """
        matrixInt = []
        with open(filename, "r") as file:
            for line in file: matrixInt.append(line.strip().split())

        for listInt in matrixInt:
            for i in range(len(listInt)):
                listInt[i] = int(listInt[i])
        
        #check format
        key = len(matrixInt[0])
        if any(len(row)!=key for row in matrixInt):
            raise ValueError("The number of integers in this matrix is not consistent from row to row")
        else: 
            #Flatten the 2d array into a 1d array
            flattened_matrix = flatten(matrixInt)
            #Set variables for init
            self._num_rows = len(matrixInt)
            self._num_cols = len(matrixInt[0])
            self._data = flattened_matrix

    def __init__(self, num_rows: int = None, num_cols: int = None, data: list[int] = None,*, filename:str = None) -> None:
        if num_rows is not None:
            #call private helper passing num rows, num_cols, data
            self._directData(num_rows, num_cols, data)
        else:
            #call private helper to read a file
            self._readFile(filename)

    def getNumRows(self)->int:
        """_summary_ This function returns the number of rows in the matrix

        Returns:
            int: returns at integer of the number of rows in the matrix
        """
        return self._num_rows
    
    def getNumCols(self)->int:
        """_summary_ This function returns the number of cols in the specified matrix

        Returns:
            int: returns an int of the number of columns in the matrix
        """
        return self._num_cols
    
    def __str__(self)->str:
        """_summary_ This function prints out a str form of the matrix in the correct format 

        Returns:
            str: returns a str of the matrix in correct format and lets the user see what the matrix looks like
        """
        max_width = max(len(str(item)) for item in self._data)
        result = []
        for i in range(self._num_rows):
            #slicing the each row. The index starts at i*self._num_cols (inclusive) stops before (i+1)*self._num_cols which is the next row
            row = self._data[i * self._num_cols: (i + 1) * self._num_cols]
            row_str = "|  "
            for item in row:
                num_spaces = max_width - len(str(item))
                for i in range(num_spaces):
                    row_str+= " "
                row_str += str(item) + "  " 
            row_str += "|"
            result.append(row_str)
        return "\n".join(result)
    
    def __eq__(self, other: 'Matrix')-> bool:
        """_summary_ This class function determines whether two matrices are equal based off number of rows, columns, and data inside
        Args:
            other (Matrix): The second matrix

        Returns:
            bool: returns true or false based on if two matrices are equal
        """
        isEqual = None
        if self.getNumCols() == other.getNumCols() and self.getNumRows() == other.getNumRows():
            if self._data == other._data:
                isEqual = True
            else: isEqual = False
        else: isEqual = False
        return isEqual

    def __getitem__(self, row_col: tuple[int])->int:
        """_summary_ This function returns the item as the specified position, row, col and if it is out of bounds it raises a indexerror

        Args:
            row_col (tuple[int]): row, col user specified of number they want in matrix

        Raises:
            IndexError: row is out of bounds of the matrix
            IndexError: col is out of bounds of the matrix

        Returns:
            int: returns the item as row, col
        """
        row, col = row_col
    
        if row == -1 and col == -1:
            item = self._data[-1]
        else:
            if row <0 or row > self._num_rows:
                raise IndexError(f"Specified Row: {row} is out of range of matrix")
            if col < 0 or col > self._num_cols:
                raise IndexError(f"Specified Column: {col} is out of range of the matrix")
            index = row * self._num_cols + col
            item = self._data[index]
        return item

    def __add__(self, other: 'Matrix')-> 'Matrix':
        """_summary_ adds two matrices that are of equal size meaning same number of cols and same number of rows

        Args:
            other (Matrix): matrix you want to add

        Raises:
            ValueError: size of matrices are different

        Returns:
            Matrix: the sum of the two matrices
        """
        addedList = []
        if(self.getNumCols() == other.getNumCols() and self.getNumRows() == other.getNumRows()):
            for i in range(len(self._data)):
                addedList.append(self._data[i]+other._data[i])
        else:
            raise ValueError(f"The dimensons of the two provided matrices are not equal and therefore cannot be added")
        newMatrix = Matrix(self._num_rows, self._num_cols, addedList)
        return newMatrix

    def transpose(self)->'Matrix':
        """_summary_ transposing a function basically just flips the rows and columns. So numbers that were in a row are now in a col and the numbers that were in a col are now in a row

        Returns:
            Matrix: tranposed function
        """
        transposeList = [None]*(self._num_rows*self._num_cols)
        for row in range(self._num_rows):
            for col in range(self._num_cols):
                originalIndex = row * self._num_cols + col
                transposeIndex = col * self._num_rows + row
                transposeList[transposeIndex] = self._data[originalIndex]
        transposeMatrix = Matrix(self._num_cols, self._num_rows, transposeList)
        return transposeMatrix

    def __mul__(self, other: 'Matrix')->'Matrix':
        """_summary_ multiples two matrices and if the number of rows doesn't equal the number of columns from the first matrix to the second it raises a valueerror

        Args:
            other (Matrix): matrix you want to multiply to the first

        Raises:
            ValueError: rows doesn't equal columns between the matrices

        Returns:
            Matrix: multipled matrix
        """
        multList = [None]*(self._num_rows*other._num_cols)
        if self._num_cols != other._num_rows:
            raise ValueError("Dimensons of the matrices are not suitable to be multiplied. Rows does not equal columns.")
        else:
            for i in range(self._num_rows):
                for j in range(other._num_cols):
                    dotProduct = 0
                    for k in range(self._num_cols):
                        dotProduct+= self._data[i*self._num_cols+k]*other._data[k*other._num_cols+j]
                    multList[i*other._num_cols+j] = dotProduct
        multMatrix = Matrix(self._num_rows, other._num_cols, multList)
        return multMatrix
    
def flatten(twod_data: list[list[int]])->list[int]:
    """_summary_

    Args:
        twod_data (list[list[int]]): 2d array from file

    Returns:
        list[int]: returns 1d array so str can translate into a print
    """
    flatten_list = []
    for list in twod_data:
        for number in list:
            flatten_list.append(number)
    return flatten_list

def main()-> None:

    #Testing functions
    m1 = Matrix(3,2,[1,2,3,456,5,6])
    m2 = Matrix(filename = "MatrixTest.txt")
    m3 = Matrix(6,4,[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])
    m4 = Matrix(3,2,[1,2,3,456,5,6])
    m5 = Matrix(2,3,[6,5,3,3,2,1])

    #getNumRows test
    print(f"Testing getNumRows function for \n{m1}: number of rows is {m1.getNumRows()} and expected number is 3")
    print(f"Testing getNumRows function for \n{m2}: number of rows is {m2.getNumRows()} and expected number is 3")
    print(f"Testing getNumRows function for \n{m3}: number of rows is {m3.getNumRows()} and expected number is 6")

    #getNumCols test
    print(f"Testing getNumCols function for \n{m1}: number of cols is {m1.getNumCols()} and expected number is 2")
    print(f"Testing getNumCols function for \n{m2}: number of cols is {m2.getNumCols()} and expected number is 2")
    print(f"Testing getNumCols function for \n{m3}: number of cols is {m3.getNumCols()} and expected number is 4")
    
    #__str__ test
    print(f"Testing __str__ function for m1 data: {m1._data}: this prints \n{m1.__str__()}")
    print(f"Testing __str__ function for m2_data: {m2._data}: this prints \n{m2.__str__()} ")
    print(f"Testing __str__ function for m3_data: {m3._data}: this prints \n{m3.__str__()}")

    #__eq__ test
    print(f"Testing __eq__ function for m1 = m2 expected = False. Actual result = {m1.__eq__(m2)}")
    print(f"Testing __eq__ function for m1 = m3 expected = False. Actual result = {m1.__eq__(m3)}")
    print(f"Testing __eq__ function for m2 = m3 expected = False. Actual result = {m2.__eq__(m3)}")
    print(f"Testing __eq__ function for m1 = m4 expected = True. Actual result = {m1.__eq__(m4)}")

    #__getItem__ test
    print(f"Testing __getItem__ function for \n{m1} expected number at position (row: 0, col: 1) is 2. Actual result is {m1.__getitem__([0,1])}")
    print(f"Testing __getItem__ function for \n{m2} expected number at position (row: 2, col: 1) is 6. Actual result is {m2.__getitem__([2,1])}")
    print(f"Testing __getItem__ function for \n{m3} expected number at position (row: 4, col: 1) is 18. Actual result is {m3.__getitem__([4,1])}")
    try:
        print(f"Testing __getItem__ function for \n{m1} expected number at position (row: 4, col: 1) is error outofbounds. Actual result is {m1.__getitem__([4,1])}")
    except IndexError as error:
        print(f"Error for m1: {error}")
    try:
        print(f"Testing __getItem__ function for \n{m2} expected number at position (row: 2, col: -1) is error outofbounds. Actual result is {m1.__getitem__([2,-1])}")
    except IndexError as error:
        print(f"Error for m2: {error}")

    #__add__ test
    print(f"Testing __add__ function for \n{m1}\n+\n{m2}: result is \n{m1.__add__(m2)}")
    print(f"Testing __add__ function for \n{m1}\n+\n{m4}: result is \n{m1.__add__(m4)}")
    print(f"Testing __add__ function for \n{m4}+\n{m4}: result is \n{m4.__add__(m4)}")
    try:
        print(f"Testing __add__ function for \n{m1}\n+\n{m3}: result is \n{m1.__add__(m3)}")
    except ValueError as error:
        print(f"Error for m1+m3: {error}")

    #transpose test
    print(f"Testing transpose function for \n{m1}: transpose is \n{m1.transpose()}")
    print(f"Testing transpose function for \n{m2}: transpose is \n{m2.transpose()}")
    print(f"Testing transpose function for \n{m3}: transpose is \n{m3.transpose()}")

    #__mul__ test
    print(f"Testing multiplcation function for \n{m1} * \n{m5}: result is \n{m1.__mul__(m5)}")
    print(f"Testing multiplcation function for \n{m2} * \n{m5}: result is \n{m2.__mul__(m5)}")
    print(f"Testing multiplcation function for \n{m4} * \n{m5}: result is \n{m4.__mul__(m5)}")
    try:
        print(f"Testing __mul__ function for \n{m1}\n+\n{m3}: result is \n{m1.__mul__(m3)}")
    except ValueError as error:
        print(f"Error for m1*m3: {error}")

if __name__ == "__main__":
    main()
    


