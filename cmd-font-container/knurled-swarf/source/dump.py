import sys, swarf
def dump(cells, chars, H, per=16):
    chars=[c for c in chars if c in cells]
    for k in range(0,len(chars),per):
        grp=chars[k:k+per]
        print('   '.join(c.ljust(max(cells[c].w,1)) for c in grp))
        for y in range(H):
            print('   '.join(''.join('#' if v else '.' for v in cells[c].rows[y]).ljust(max(cells[c].w,1)) for c in grp))
        print()
if __name__=='__main__':
    p=int(sys.argv[1]); chars=sys.argv[2]
    ms,reg,bold=swarf.all_sizes()
    dump(reg[p], chars, p, int(sys.argv[3]) if len(sys.argv)>3 else 16)
