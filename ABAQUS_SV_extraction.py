
"""
Programme :  ABAQUS_SV_extraction.py

Pouya TAJDARY

Mai 2018

Description :

Find state variables from the element set.

Commande : 

abq2017 python ABAQUS_SV_extraction.py -odb "OdbName" -elset "ElsetName" 


Details :

-odb : nom du fichier .odb

-elset : nom du set d elements pour lequel les resultats doivent etre recuperes


"""

#--------------------------------------------------------------------

from odbAccess import *

#--------------------------------------------------------------------

def ABAQUS_SV_extraction(OdbName, ElsetName):
    print ' '
    print 'Read'


    FileName = OdbName+'.dat'
    File = open(FileName,'w')
    Odb = openOdb(OdbName)

    
    StepPath = Odb.steps
    Elmts = Odb.rootAssembly.instances['PART-1-1'].elementSets[ElsetName]
    NbElmts = len(StepPath.values()[0].frames[0].fieldOutputs['LE'].getSubset(region=Elmts).values)
    print 'Number of elements: '+str(NbElmts)

    
    NbSteps = len(StepPath)
    print 'Number of steps: '+str(NbSteps)

    for StepCount in range (0,NbSteps):
        FramePath = StepPath.values()[StepCount]
        print StepPath.keys()[StepCount]

        
        NbFrames = len(FramePath.frames)
        print 'Number of frames: '+str(NbFrames)

        
        for FrameCount in range(0, NbFrames):
            FieldOutputFrameValuePath = FramePath.frames[FrameCount]
            print 'Frame '+str(FrameCount)
            print FieldOutputFrameValuePath.description

            EpsilonPath = FieldOutputFrameValuePath.fieldOutputs['LE'].getSubset(region=Elmts)
            SigmaPath = FieldOutputFrameValuePath.fieldOutputs['S'].getSubset(region=Elmts)
            COORD = FieldOutputFrameValuePath.fieldOutputs['COORD'].getSubset(region=Elmts)
            Tps = FieldOutputFrameValuePath.frameValue

            
            for ElmtCount in range(0, NbElmts):
                Exx = EpsilonPath.values[ElmtCount].data[(0)]
                Sxx = SigmaPath.values[ElmtCount].data[(0)]
                C1 = COORD.values[ElmtCount].data[(0)]
                Eyy = EpsilonPath.values[ElmtCount].data[(1)]
                Syy = SigmaPath.values[ElmtCount].data[(1)]
                C2 = COORD.values[ElmtCount].data[(1)]
                Exy = EpsilonPath.values[ElmtCount].data[(4)]
                Sxy = SigmaPath.values[ElmtCount].data[(4)]
                C3 = COORD.values[ElmtCount].data[(2)]

                
                File.write('%f %f %f \n' %(Eyy, C1, C2))


    Odb.close()

#--------------------------------------------------------------------
#--------------------------------------------------------------------
if __name__ == '__main__':

    OdbName = ElsetName = None
    ArgList = argv
    ArgNb = len(ArgList)
    print ' '
    print 'Start'
    i=1

    while (i < ArgNb):

        if (ArgList[i][:2] == "-o"):

            i += 1
            OdbName = ArgList[i]
            i +=1
            print '-odb'

        elif (ArgList[i][:2] == "-e"):

            i += 1
            ElsetName = ArgList[i]
            i += 1
            print '-elset'

        elif (ArgList[i][:2] == "-d"):

            i += 1
            DirNb = ArgList[i]
            i += 1
            print '-dir'

    if not (ElsetName):
        ElsetName = 'ETOUT'
        print '-elset default'

    ABAQUS_SV_extraction(OdbName, ElsetName)
