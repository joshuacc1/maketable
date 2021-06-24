class te:
    '''
    Enumeration of table elements.

    ...

    Attributes
    ----------
    corners: list
        list of corner character integers
    sides: list
        list of side character integers
    middle: int
        four corner intersection character integer

    cul:
        corner upper left
    cur:
        corner upper right
    cdl:
        corner bottom left
    cdr:
        corner bottom right

    su:
        side up
    sd:
        side down
    sl:
        side left
    sr:
        side right

    sud:
        side up divider
    sdd:
        side down divider
    sld:
        side left divider
    srd:
        side right divider

    m:
        four corner intersection character

    '''

    def __init__(self):
        self.corners=[9484,9488,9492,9496]
        self.sides=[9472,9474,9500,9508,9516,9524]
        self.middle=9532

        self.cul=chr(self.corners[0])
        self.cur=chr(self.corners[1])
        self.cdl=chr(self.corners[2])
        self.cdr=chr(self.corners[3])

        self.su=chr(self.sides[0])
        self.sud=chr(self.sides[4])
        self.sd=chr(self.sides[0])
        self.sdd=chr(self.sides[5])
        self.sr=chr(self.sides[1])
        self.srd=chr(self.sides[3])
        self.sl=chr(self.sides[1])
        self.sld=chr(self.sides[2])

        self.m=chr(self.middle)

def top(size:int,divider:bool,ledge=None,redge=None):
    """

    :param size: size of the cell
    :param divider: A divider character for a cell
    :param ledge: Left edge character
    :param redge: Right edge character
    :return: String of divider element
    """

    c=te()
    s=''
    if ledge: s+=ledge
    s+=c.su*size
    if redge: s+=redge
    return s

def row(size:int,value,centered,ledge=None,redge=None):
    """

    :param size: size of the cell
    :param value: value in a cell element
    :param centered: makes the value centered
    :param ledge: Left edge character
    :param redge: Right edge character
    :return: String of divider element
    """

    c=te()
    s=''
    if ledge: s+=ledge
    vsize=len(str(value))
    padding=size-vsize
    if centered:
        lpad=int(padding/2)
        rpad=padding-lpad
        s+=lpad*' ' + str(value) + rpad*' '
    else:
        lpad=1
        rpad=padding-1
        s+=lpad*' ' + str(value) + rpad*' '
    if redge: s+=redge
    return s

def div(size:int,divider:None,ledge=None,redge=None):
    """

    :param size: size of the cell.
    :param divider: A divider character for a cell.
    :param ledge: Left edge character.
    :param redge: Right edge character.
    :return: String of divider element.

    """

    c=te()
    s=''
    if ledge: s+=ledge
    if divider:
        nsize=size-1
        lsize=int(nsize/2)
        rsize=nsize-lsize
        s+=lsize*c.su+divider+rsize*c.su
    else:
        s+=c.su*size
    if redge: s+=redge
    return s

class template:
    '''Establishes a table template for output'''
    def __init__(self,centered:bool):
        c=te()
        self.rowsize=5

        cfa = c.sud if centered else None
        self.topleft=lambda rowsize: div(rowsize,cfa,c.cul)
        self.topmid=lambda rowsize: div(rowsize,cfa,c.sud)
        self.topright=lambda rowsize: div(rowsize,cfa,c.sud,c.cur)

        cfb = c.m if centered else None
        self.midleft=lambda rowsize: div(rowsize,cfb,c.sld)
        self.midmid=lambda rowsize: div(rowsize,cfb,c.m)
        self.midright=lambda rowsize: div(rowsize,cfb,c.m,c.srd)

        self.rowleft=lambda x,rowsize: row(rowsize,x,centered,c.sl)
        self.rowmid=lambda x,rowsize: row(rowsize,x,centered,c.sr)
        self.rowright=lambda x,rowsize: row(rowsize,x,centered,c.sr,c.sr)

        cfc = c.sdd if centered else None
        self.bottomleft=lambda rowsize: div(rowsize,cfc,c.cdl)
        self.bottommid=lambda rowsize: div(rowsize,cfc,c.sdd)
        self.bottomright=lambda rowsize: div(rowsize,cfc,c.sdd,c.cdr)

    def render(self,table:list,labels=None,padding=6):
        """
        :param table: Table of values.
        :param labels: Table of column labels.
        :param padding: Number of spaces to pad on both sides of the value in a cell.
        :return: string of table
        """

        c=te()
        if labels:
            if len(table[0])==len(labels):
                table.insert(0,labels)
            else:
                raise(Exception('Row and label size mismatch'))

        if not len(set([len(x) for x in table]))==1:
            raise(Exception('Rows do not have equal number of elements'))

        maxcolumnsizes=[max([len(str(x[y]))+padding for x in table]) for y in range(len(table[0]))]
        tablestring=''
        tablestring+=self.topleft(maxcolumnsizes[0])
        for maxcolsize in maxcolumnsizes[1:len(maxcolumnsizes)-1]:
            tablestring+=self.topmid(maxcolsize)
        tablestring+=self.topright(maxcolumnsizes[-1]) if len(maxcolumnsizes)>1 else c.cur
        tablestring+='\n'
        for row in table:
            tablestring+=self.rowleft(row[0],maxcolumnsizes[0])
            for column in enumerate(row[1:]):
                columnvalue=column[1]
                columnindex=column[0]
                if columnvalue == row[-1]:
                    tablestring+=self.rowright(columnvalue,maxcolumnsizes[columnindex+1])
                    continue
                tablestring+=self.rowmid(columnvalue,maxcolumnsizes[columnindex+1])
            if not len(row)>1: tablestring += c.sl
            tablestring+='\n'
            if row==table[0]:
                tablestring+=self.midleft(maxcolumnsizes[0])
                for maxcolsize in maxcolumnsizes[1:len(maxcolumnsizes)-1]:
                    tablestring+=self.midmid(maxcolsize)
                tablestring+=self.midright(maxcolumnsizes[-1]) if len(row)>1 else c.sl
                tablestring+='\n'

        tablestring+=self.bottomleft(maxcolumnsizes[0])
        for maxcolsize in maxcolumnsizes[1:len(maxcolumnsizes)-1]:
            tablestring+=self.bottommid(maxcolsize)
        tablestring+=self.bottomright(maxcolumnsizes[-1])  if len(row)>1 else c.cdr
        return tablestring

def make_table(rows: list,labels=None,centered: bool = False):
    """
    :param rows: 2D list containing objects that have a single-line representation (via 'str')
    All rows must be of the same length.
    :param labels: List containing the column labels. If present, the length must equal to that of each row.
    :param centered: If the items should be aligned to the center, else they are left aligned.
    :return: A table representing the rows passed in.
    """

    t=template(centered)
    return t.render(rows,labels,6)
