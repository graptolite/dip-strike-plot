import pandas as pd
import numpy as np
from matplotlib import cm,colors

import config

svg = lambda svg : """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg">
%s
</svg>""" % svg

svg_group = lambda name,grouped_svg : """<g id=\"%s\">
%s
</g>""" % (name,grouped_svg)

def deg2rad(deg):
    return (deg/360) * 2 * np.pi

def letter2bearing(letter_dir):
    try:
        dir_dict = {"n":0,
                    "e":90,
                    "s":180,
                    "w":270}
        if "w" in letter_dir:
            dir_dict["n"] = 360
        bearing = sum([dir_dict[letter] for letter in letter_dir]) / len(letter_dir)
    except TypeError:
        return None
    return bearing

def standardise_strike(strike,dip,dip_dir):
    dip_right = (strike + 90)%360
    dip_left = (strike - 90)%360
    if dip_dir == "" and dip == 90:
        # doesn't really matter
        RH_rule_strike = strike
    elif dip_dir == "" and dip == 0:
        # doesn't really matter
        RH_rule_strike = strike
    elif dip_dir != "":
        diff_dip_right = abs(dip_dir - dip_right)
        diff_dip_left = abs(dip_dir - dip_left)
        if diff_dip_right < diff_dip_left:
            # dip is clockwise of strike so is fine
            RH_rule_strike = strike
        else:
            RH_rule_strike = (strike + 180) % 360
    else:
        # nullify data
        RH_rule_strike = np.nan
    return RH_rule_strike

def join_points(p1,p2):
    # plot straight line that joins the two points p1 and p2
    return [p1[0],p1[1],p2[0],p2[1]]

def plot_dip_strike(easting,northing,strike,dip,path_id,colour="#000000",origin=[0,0],downscale=1,plane_type="bedding"):
    path = lambda x0,y0,x1,y1,path_id,width=0.05,colour="#000000" : """<path style="fill:none;stroke:%s;stroke-width:%fpx;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1" d="M %f,%f %f,%f" id="%s"/>""" % (colour,width/downscale,x0,y0,x1,y1,path_id)

    text = lambda x,y,text,text_id,colour="#000000" : """<text style="font-size:%(font_size)f;line-height:0;font-family:sans-serif;-inkscape-font-specification:'sans-serif, Normal';letter-spacing:0px;word-spacing:0px;fill:%(colour)s;fill-opacity:1;" x="%(x)f" y="%(y)f" id="%(text_id)s">
<tspan id="tspan-%(text_id)s" x="%(x)f" y="%(y)f" style="stroke-width:%(font_width)f">%(text)s</tspan>
</text>""" % {"x":x,"y":y,"text_id":text_id,"text":text,"colour":colour,"font_size":1/downscale,"font_width":.4/downscale}

    line_length = 5/downscale
    half_line_length = line_length/2

    e_n = ((np.array([easting,northing]) - np.array(origin)) / downscale) * np.array([1,-1])

    p = half_line_length * np.array([np.sin(-deg2rad(strike)),np.cos(-deg2rad(strike))]) # (x,y) of one end of the strike line assuming the center is (0,0)

    p_d = half_line_length * np.array([np.sin(-deg2rad(strike + 90)),np.cos(-deg2rad(strike + 90))]) # (x,y) of the end of the dip line assuming the center is (0,0)

    e_n_p1 = e_n + p # (n,e) of one end of the strike line
    e_n_p2 = e_n - p # (n,e) of the other end of the strike line

    if dip!="":
        if int(dip) == 90:
            d0 = e_n + 0.5 * p_d
            d1 = e_n - 0.5 * p_d
        elif int(dip) == 0:
            d0 = e_n + p_d
            d1 = e_n - p_d
        else:
            d0 = e_n
            d1 = e_n - p_d # (n,e) of the end of the dip line

        if plane_type == "bedding":
            dip_line = beddind_dip_line = path(*join_points(d0,d1),"dip-" + path_id,colour=colour)
        elif plane_type == "foliation":
            foliation_dip_double_spacing_factor = 0.1
            foliation_dip_double_spacing = p*foliation_dip_double_spacing_factor
            dip_line = path(*join_points(d0+foliation_dip_double_spacing,d1+foliation_dip_double_spacing),"fol1-" + path_id,colour=colour) + path(*join_points(d0-foliation_dip_double_spacing,d1-foliation_dip_double_spacing),"fol2-" + path_id,colour=colour)
        elif plane_type == "vein":
            joint_dip_double_spacing_factor = 0.3
            joint_dip_double_spacing = p*joint_dip_double_spacing_factor
            dip_line = path(*join_points(d0,d1),"vein-" + path_id,colour=colour,width=0.5) + path(*join_points(d0+joint_dip_double_spacing,d1),"vein1-" + path_id,colour=colour) + path(*join_points(d0-joint_dip_double_spacing,d1),"vein2" + path_id,colour=colour)
        elif plane_type == "joint":
            joint_dip_double_spacing_factor = 0.3
            joint_dip_double_spacing = p*joint_dip_double_spacing_factor
            dip_line = path(*join_points(d0+joint_dip_double_spacing,d1),"joint1-" + path_id,colour=colour) + path(*join_points(d0-joint_dip_double_spacing,d1),"joint2" + path_id,colour=colour)
        else:
            print("invalid plane type, defaulting to bedding")
            dip_line = bedding_dip_line
        dip_mag = text(e_n[0],e_n[1],str(int(dip)),"text-" + path_id,colour=colour)
    else:
        dip_line = ""
        dip_mag = ""

    strike_line = path(*join_points(e_n_p1,e_n_p2),"strike-" + path_id,colour=colour)
    return svg_group("group-" + path_id,"\n".join([strike_line,dip_line,dip_mag]))

def plot_data(datafile):
    df = pd.read_csv(datafile,delimiter=",").fillna("")
    plot_df = df
    df["easting"] = df["easting"].apply(float)
    df["northing"] = df["northing"].apply(float)

    normalise = lambda i : int(i*(cm.rainbow.N/10) % cm.rainbow.N)
    cmap = lambda i : colors.to_hex(cm.rainbow(normalise(i)))

    origin = np.array([min(df["easting"]),min(df["northing"])])

    combined_svg = ""
    for plane_type in set(df["plane_type"]): # out of foliation, bedding, vein, joint (at least for now)
        dipstrikes = []
        plane_df = plot_df[plot_df["plane_type"]==plane_type]
        for i in plane_df.index:
            data = plot_df.iloc[i]
            easting = data["easting"]
            northing = data["northing"]
            dip = data["dip"]
            dip_dir = data["dip direction"]
            strike = data["strike"]
            if dip_dir:
                strike = standardise_strike(strike+config.MAGNETIC_CORRECTION,dip,letter2bearing(dip_dir))

            if easting and northing and strike:
                dipstrike = plot_dip_strike(easting,northing,strike,dip,"dipstrike" + str(i),cmap(i),origin=origin,downscale=1,plane_type=plane_type)
                dipstrikes.append(dipstrike)
        combined_svg += svg_group(plane_type,"\n".join(dipstrikes))

    return combined_svg

dipstrike_svgs = plot_data(config.DATA_FILE)

with open(config.SVG_FILE,"w") as outfile:
    outfile.write(svg(dipstrike_svgs))