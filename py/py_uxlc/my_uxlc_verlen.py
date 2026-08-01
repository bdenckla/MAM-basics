import py_uxlc.my_uxlc_cvp as cvp


def get_verlen(uxlc, std_bkid, the_cvp):
    book = uxlc[std_bkid]
    chnu, vrnu = cvp.chapnver(the_cvp)
    return len(book[chnu - 1][vrnu - 1])
