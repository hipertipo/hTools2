
def interpolate_node(offset, bpoint, bpoint_prev, bpoint_next):

    # get bcp handles as absolute coordinates
    bpoint_bcpin_abs       = bpoint.anchor[0]      + bpoint.bcpIn[0],       bpoint.anchor[1]      + bpoint.bcpIn[1]
    bpoint_bcpout_abs      = bpoint.anchor[0]      + bpoint.bcpOut[0],      bpoint.anchor[1]      + bpoint.bcpOut[1]
    bpoint_next_bcpin_abs  = bpoint_next.anchor[0] + bpoint_next.bcpIn[0],  bpoint_next.anchor[1] + bpoint_next.bcpIn[1]
    bpoint_prev_bcpout_abs = bpoint_prev.anchor[0] + bpoint_prev.bcpOut[0], bpoint_prev.anchor[1] + bpoint_prev.bcpOut[1]

    # adjust next segment
    if bpoint.type:

        add_in_x  = 0
        add_out_x = 0
        xdiff     = bpoint_next.anchor[0] - float(bpoint.anchor[0])

        if xdiff != 0:
            add_in_x  = ( (bpoint_next.anchor[0] - bpoint_next_bcpin_abs[0] ) / xdiff ) * offset[0]
            add_out_x = ( (bpoint_next.anchor[0] - bpoint_bcpout_abs[0] )     / xdiff ) * offset[0]

        add_in_y  = 0
        add_out_y = 0
        ydiff     = bpoint_next.anchor[1] - float(bpoint.anchor[1])

        if ydiff != 0:
            add_in_y  = ( (bpoint_next.anchor[1] - bpoint_next_bcpin_abs[1] ) / ydiff ) * offset[1]
            add_out_y = ( (bpoint_next.anchor[1] - bpoint_bcpout_abs[1]     ) / ydiff ) * offset[1]

        bpoint_next.bcpIn = ( bpoint_next.bcpIn[0] + add_in_x,  bpoint_next.bcpIn[1] + add_in_y  )
        bpoint.bcpOut     = ( bpoint.bcpOut[0]     + add_out_x, bpoint.bcpOut[1]     + add_out_y )

    # adjust previous segment
    if bpoint.type:

        add_in_x  = 0
        add_out_x = 0
        xdiff     = bpoint_prev.anchor[0] - float(bpoint.anchor[0])

        if xdiff != 0:
            add_in_x  = ( (bpoint_prev.anchor[0] - bpoint_bcpin_abs[0])       / xdiff ) * offset[0]
            add_out_x = ( (bpoint_prev.anchor[0] - bpoint_prev_bcpout_abs[0]) / xdiff ) * offset[0]

        add_in_y  = 0
        add_out_y = 0
        ydiff     = bpoint_prev.anchor[1] - float(bpoint.anchor[1])

        if ydiff != 0:
            add_in_y  = ( (bpoint_prev.anchor[1] - bpoint_bcpin_abs[1])       / ydiff ) * offset[1]
            add_out_y = ( (bpoint_prev.anchor[1] - bpoint_prev_bcpout_abs[1]) / ydiff ) * offset[1]

        bpoint.bcpIn       = ( bpoint.bcpIn[0]       + add_in_x,  bpoint.bcpIn[1]       + add_in_y  )
        bpoint_prev.bcpOut = ( bpoint_prev.bcpOut[0] + add_out_x, bpoint_prev.bcpOut[1] + add_out_y )

    bpoint.anchor = (bpoint.anchor[0] + offset[0], bpoint.anchor[1] + offset[1])

def nudge_selected(offset, g):
    g.prepareUndo('nudge selected')
    for c in g:
        previousbpoint = None
        bpoint_next     = None
        i = 0
        for bpoint in c.bpoints:
            if i != 0:
                bpoint_prev = c.bpoints[i-1]
            else:
                bpoint_prev = c.bpoints[len(c.bpoints)-1]
            if i + 1 != len(c.bpoints):
                bpoint_next = c.bpoints[i+1]
            else:
                bpoint_next = c.bpoints[0]
            if bpoint.selected:
                interpolateNode(offset, bpoint, bpoint_prev, bpoint_next)
            i += 1
    g.performUndo()
