import lecroyparser
import matplotlib.pyplot as plt
import numpy as np
import os
from ROOT import *

ToTList = []
AmplitudeList = []
c1 = TCanvas("","",800,600)
AmplitudeHist = TH1F("Amplitude","",50,-55,-45)

for eventIndex in range(700):
    path = "/home/cz/tdc/0913/C4--XX--%05d.trc"%(eventIndex)
    data = lecroyparser.ScopeData(path)
    time = data.x
    amp = data.y
    TimeList = time.tolist()
    AmpList = amp.tolist()
    BinSize = len(TimeList)
    baselineC2 = 0
    indexnumC2 = 0
    for index in range(len(TimeList)):
        TimeList[index] = TimeList[index] * 1000000000 + 400
        AmpList[index] = AmpList[index] * 1000
        if TimeList[index] > 348 and TimeList[index] < 368:
            baselineC2 += AmpList[index]
            indexnumC2 += 1
    baseline = baselineC2 / indexnumC2
    for index in range(len(TimeList)):
        AmpList[index] = AmpList[index] - baseline

    TimeList = np.array(TimeList)
    AmpList = np.array(AmpList)

    ThreIndex = -1
    AmpIndex = -1
    AmpValueC1 = 1000
    AmpTime = 0
    for Index in range(BinSize):
        if AmpValueC1 > AmpList[Index]:
            AmpValueC1 = AmpList[Index]
            AmpIndex = Index
            AmpTime = TimeList[Index]
    AmplitudeList.append(AmpValueC1)
    AmplitudeHist.Fill(AmpValueC1)
    if AmpValueC1 > -48:
        graph1 = TGraph(len(TimeList),TimeList,AmpList)
        graph1.Draw("AC")
        graph1.GetXaxis().SetTitle("Time(ns)")
        graph1.GetXaxis().SetRangeUser(390,420)
        graph1.SetLineColor(kBlue);
        graph1.SetLineWidth(2);
        c1.SaveAs("Amplitude_{}.png".format(eventIndex))
        c1.Clear()

AmplitudeHist.Draw()
AmplitudeHist.SetLineWidth(2)
c1.SaveAs("AmplitudeHist.png")


'''         
    if AmpValueC1 < 0:
        path1 = "/home/cz/tdc/0913/C4--XX--%05d.trc" % (eventIndex)
        data1 = lecroyparser.ScopeData(path1)
        amp1 = data1.y
        AmpList1 = amp1.tolist()
        baseline = 0
        indexnum = 0
        for index in range(len(TimeList)):
            AmpList1[index] = AmpList1[index] * 1000
            if TimeList[index] > 348 and TimeList[index] < 368:
                baseline += AmpList1[index]
                indexnum += 1
        baseline = baseline / indexnum
        for index in range(len(TimeList)):
            AmpList1[index] = AmpList1[index] - baseline

        ThreIndex = -1
        AmpIndex = -1
        AmpValueC2 = 1000
        for Index in range(BinSize):
            if AmpList1[Index] < -5:
                ThreIndex = Index
                break
        if ThreIndex > 0:
            for Index in range(ThreIndex,BinSize-2):
                if AmpList1[Index] < AmpList1[Index + 1] < AmpList1[Index + 2] and AmpList1[Index] < AmpList1[Index - 1] < AmpList1[Index - 2]:
                    AmpIndex = Index
                    AmpValueC2 = AmpList1[Index]
                    break

        ToTList.append(AmpValueC1)
        AmplitudeList.append(AmpValueC2)


plt.scatter(ToTList, AmplitudeList, c='green',marker = '.')
plt.ylim(-23.6, -24.2)
plt.xlim(-23.9, -24.5)
plt.legend()
#plt.xlabel('ToT/ns')
plt.xlabel('Amplitude/mV')
plt.ylabel('Amplitude/mV')
#plt.text(475, -0.8, str(AmpValue), fontsize=18,
'''
