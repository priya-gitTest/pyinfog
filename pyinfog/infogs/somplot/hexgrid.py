# Copyright 2017-2018 Niall McCarroll
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pyinfog.svg.pysvg import polygon,sector,circle,text,javascript_snippet

from math import radians,sin,cos,pi

class HexGrid(object):

    def __init__(self,width,height,max_distance,plot):
        self.gx =width 
        self.gy =height
        self.max_distance = max_distance
        self.distances = {}
        self.plot = plot

        for d in range(0,self.max_distance+1):
            for xc in range(0,self.gx):
                for yc in range(0,self.gy):
                    self.genDistance(xc,yc,xc,yc,0,d)
        
    def position(self,xc,yc,xd,yd):
        pos = str(xc) + "."
        pos += str(yc) + "."
        pos += str(xd) + "."
        pos += str(yd)
        return pos

    def putDistance(self,xc,yc,xd,yd,d):
        self.distances[self.position(xc,yc,xd,yd)] = d
    
    def getDistance(self,xc,yc,xd,yd):
        key = self.position(xc,yc,xd,yd)
        if key in self.distances:
            return self.distances[key]
        else:
            return None

    def neighbours(self,x,y):
        n_list = []
        n_list.append(((x-1) % self.gx,y))
        n_list.append(((x+1) % self.gx,y))
        n_list.append((x, (y+1) % self.gy))
        n_list.append((x, (y-1) % self.gy))
        if x % 2 == 0:
            n_list.append(((x-1) % self.gx,(y+1) % self.gy))
            n_list.append(((x-1) % self.gx,(y-1) % self.gy))
        else:
            n_list.append(((x+1) % self.gx,(y+1) % self.gy))
            n_list.append(((x+1) % self.gx,(y-1) % self.gy))
        return n_list 

    def genDistance(self,xc,yc,xd,yd,r,d):
        if r == d:
            if self.getDistance(xc,yc,xd,yd) == None:
                self.putDistance(xc,yc,xd,yd,r)
        else:
            n_list = self.neighbours(xd,yd)
            for (nx,ny) in n_list:
                self.genDistance(xc,yc,nx,ny,r+1,d)

    def render(self,d,ox,oy,dlength,scores):
        self.renderGrid(d,ox,oy,dlength,scores)

    def hexagon(self,origin,dlength,rgbfill,rgbstroke,id):
        points = []
        rangle = radians(30)
        off_sm = dlength*sin(rangle)
        off_lg = dlength*cos(rangle)
        (x,y) = origin
        x -= off_lg
        y -= off_sm+dlength/2
        points.append((x,y))
        y += dlength
        points.append((x,y))
        y += off_sm
        x += off_lg
        points.append((x,y))
        y -= off_sm
        x += off_lg
        points.append((x,y))
        y -= dlength
        points.append((x,y))
        y -= off_sm
        x -= off_lg
        points.append((x,y))
        return polygon(points,rgbfill,rgbstroke,4,id)
    
    def hexacenter(self,origin,x,y,dlength):
        (ox,oy) = origin
        rangle = radians(30)
        off_sm = dlength*sin(rangle)
        off_lg = dlength*cos(rangle)
        yc = oy + (float(y)*(dlength+off_sm))+(0.5*float(dlength))+off_sm  
        xc = ox + ((float(x)+0.5)*(2*off_lg))
        if y % 2 == 1:
            xc += off_lg
        return (xc,yc)

    def renderGrid(self,diagram,ox,oy,dlength,scores):
        rangle = radians(30)
        off_sm = dlength*sin(rangle)
        off_lg = dlength*cos(rangle)
        hx = ox
        labels = []
        js = javascript_snippet(
"""
function toggleVisibility(cls) {
    var found = document.getElementsByClassName(cls);
    for(var idx=0; idx<found.length; idx++) {
        if (found[idx].getAttribute("visibility") == "hidden") {
            found[idx].setAttribute("visibility","visible");
        } else {
            found[idx].setAttribute("visibility","hidden");
        }
    }
}
""")
        diagram.add(js)
        for xc in range(0,self.gx):
            hy = oy
            for yc in range(0,self.gy):
                y = hy
                x = hx
                if yc % 2 == 1:
                    x += off_lg
                poly = self.hexagon((x, y), dlength, "#E0E0E0", (128, 128, 128), str(xc) + "_" + str(yc))
                poly.addStyle("stroke","grey")
                poly.addStyle("stroke-width","3")
                cls = str(xc)+"_"+str(yc)
                poly.addAttr("onclick","toggleVisibility(\""+cls+"\")")
                diagram.add(poly)

                centroid = self.plot.getWeights(self.plot.getOutput(xc,yc))
                assigned = scores[(xc,yc)]
                if assigned:
                    centroid_sum = sum(centroid)
                    theta = 0
                    cx = x
                    cy = y - dlength / 2
                    r1 = dlength * 0.5
                    r2 = dlength * 0.7
                    r3 = r2+10
                    for idx in range(0,len(centroid)):
                        theta0 = theta
                        theta += 2*pi*centroid[idx]/centroid_sum
                        s = sector(cx,cy, 0, r1, theta0, theta,self.plot.palette[idx][0])
                        s.addStyle("fill",self.plot.palette[idx][1])
                        s.addAttr("onclick", "toggleVisibility(\"" + cls + "\")")
                        diagram.add(s)

                    assigned = sorted(assigned,key=lambda x: x[1])
                    theta = 0
                    step = pi*2 / len(assigned)
                    if step > 1.0:
                        step = 1.0

                    for (label,colour) in assigned:
                        px = cx+r2*cos(theta)
                        py = cy+r2*sin(theta)
                        pxl = cx+r3*cos(theta)
                        pyl = cy+r3*sin(theta)
                        c = circle(px,py,dlength*0.1,colour,label)
                        t = text(pxl,pyl,label)
                        t.addAttr("dominant-baseline","middle")
                        t.addStyle("paint-order","stroke")
                        t.addStyle("fill",colour)
                        t.addStyle("stroke-width", "10px")
                        t.addStyle("stroke", "white")
                        if theta > pi/2 and theta < pi*1.5:
                            t.addStyle("text-anchor","end")
                            t.setRotation(theta-pi)
                        else:
                            t.addStyle("text-anchor","start")
                            t.setRotation(theta)
                        t.addAttr("visibility","hidden")
                        t.addAttr("class",cls)
                        diagram.add(c)
                        labels.append(t)
                        theta += step

                hy = hy + dlength+off_sm
            hx = hx + 2*off_lg
        for label in labels:
            diagram.add(label)
        return (ox+off_lg+self.gx*(2*off_lg)+10,oy+off_sm+(self.gy)*(dlength+off_sm)+10)

            

