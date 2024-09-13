import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import base64
from io import BytesIO
plt.rcParams["font.size"] = 12

class Tubular:
    def __init__(self, name, inD, outD, DUOM, top, low, depthUOM, grade):
        self.name = name
        self.inD = inD
        self.outD = outD
        self.top = top
        self.low = low
        self.totalLength = self.top - self.low
        self.grade = grade
        self.thickness = self.outD - self.inD
        self.summary = f"{name}\nID = {inD} {DUOM}\nOD = {outD} {DUOM}\nFrom {top} {6} to {low} {depthUOM}\nGrade = {grade}"

class Cement:
    def __init__(self, top, low, tub0, tub1):
        checkerRightWall = [tub0, tub1]
        whichTube = np.argmax([tub0.outD, tub1.outD])
        rightWall = checkerRightWall[whichTube].inD
        leftWall = min(tub0.outD, tub1.outD)
        self.horVals = np.array([leftWall, rightWall])
        self.topVals = [top, top]
        self.lowVals = [low, low]
        self.summary = "cement from\n{0} ft to {1}ft".format(top, low)
        
class Packer:
    def __init__(self):
        pass

class WellCasing:
    def __init__(self, name = None, topVerView = None, kop = None, uom='ft', depth_datum='KB', verStretchFactor = 1.05, horStretchFactor = 4):
        self.tubulars = {}
        self.cements = {}
        self.largestTub = 0
        self.deepestTub = 0
        self.cementID = 0
        self.showTubularSummary = True
        self.showCementSummary = True
        self.name = name
        self.topVerView = topVerView
        self.kop = kop
        self.verStretchFactor = verStretchFactor
        self.horStretchFactor = horStretchFactor
        self.uom = uom
        self.depth_datum = depth_datum
       
    def addTubular(self, tub: Tubular):
        try:
            assert tub.name not in self.tubulars.keys()
            self.tubulars[tub.name] = {"xy":np.array([tub.inD, tub.low]), "width":tub.thickness, "height":tub.totalLength, 
                                       "outD": tub.outD, "summary": tub.summary, "low": tub.low, "grade":tub.grade}            
            if tub.outD > self.largestTub:
                self.largestTub = tub.outD
            if tub.low > self.deepestTub:
                self.deepestTub = tub.low
        except:
            raise ValueError("Tubular names must be unique! that tubular has been added to this well")

    def hideTubularSummary(self):
        self.showTubularSummary = False
        
    def hideCementSummary(self):
        self.showCementSummary = False       
                            
    def visualize(self):
        stretchHorView = self.largestTub * self.horStretchFactor
        stretchVerView = self.deepestTub * self.verStretchFactor
        self.fig, self.ax = plt.subplots(figsize = (8.27, 11.69))
        # the tubulars
        for key, elem in self.tubulars.items():
            self.ax.add_patch(Rectangle(elem["xy"], elem["width"], elem["height"], color = "black"))
            self.ax.add_patch(Rectangle((-1*elem["xy"][0], elem["xy"][1]), -1*elem["width"], elem["height"], color = "black"))
            # showing tubular summaries
            if self.showTubularSummary == True:
                xText = elem["outD"] + (0.075 * stretchHorView)
                yText = elem["low"] * 0.85 
                self.ax.text(xText, yText, elem["summary"], 
                             verticalalignment = "top", horizontalalignment = "left")
    
        # the cement intervals
        for key, elem in self.cements.items():
            
            self.ax.fill_between(elem["horVals"], elem["topVals"], elem["lowVals"], color = "#6b705c")
            self.ax.fill_between(-1*elem["horVals"], elem["topVals"], elem["lowVals"], color = "#6b705c")
            # showing cement summaries
            if self.showCementSummary == True:
                xText = -elem["horVals"][1] - (0.4 * stretchHorView)
                yText = elem["lowVals"][1]
                self.ax.text(xText, yText, elem["summary"], 
                             verticalalignment = "top", horizontalalignment = "left", color = "#6b705c")
            
        self.ax.set_ylabel(f"MD {self.depth_datum} ({self.uom})")
        self.ax.set_xlim([-stretchHorView, stretchHorView])
        if self.topVerView is None:
            self.ax.set_ylim([0, stretchVerView])
        else:
            self.ax.set_ylim([self.topVerView, stretchVerView])
        
        if self.kop is not None:
            kopColor = "#0C1713"
            self.ax.hlines(self.kop, -stretchHorView, stretchHorView, linestyle = "--", color = kopColor, linewidth = 0.5, alpha = 0.75,zorder=0)
            self.ax.annotate(f"KOP at {self.kop} {self.uom}".format(self.kop), xy = (-stretchHorView + 1, self.kop - 25), color = kopColor, alpha = 0.75)

        self.ax.invert_yaxis()
        plt.tight_layout()
        
        buf = BytesIO()
        self.fig.savefig(buf, format="png")
        plt.close(self.fig)

        return buf