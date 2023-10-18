import lecroyparser
import numpy as np
from ROOT import *
import os


Amplitude2HistList = [] 
MinList = []
MinList1 = []
AmplitudeList = [-5.4,-5.3,-5.2,-5.1,-5.0]
RangeNum = len(AmplitudeList) - 1
for i in range(RangeNum):
    Amplitude2HistList.append(TH1F("Amplitude2_{}".format(i+1),"",26,-5.7,-4.6))
AmplitudeHist_2D = TH2F("Amplitude2D","",28,-5.7,-4.7,28,-5.7,-4.7)


for eventIndex in range(4000):
    path = "/home/cz/readout/test3/0927/C2--XX--%05d.trc"%(eventIndex)
    data = lecroyparser.ScopeData(path)
    time = data.x
    amp = data.y
    TimeList = time.tolist()
    AmpList = amp.tolist()
    BinSize = len(TimeList)
    baselineC2 = 0
    indexnumC2 = 0
    Min = 0
    Min1 = 0
    for index in range(len(TimeList)):
        TimeList[index] = TimeList[index] * 1000000000 + 400
        AmpList[index] = AmpList[index] * 1000
        if TimeList[index] > 300 and TimeList[index] < 320:
            baselineC2 += AmpList[index]
            indexnumC2 += 1
    baseline = baselineC2 / indexnumC2
    for index in range(len(TimeList)):
        AmpList[index] = AmpList[index] - baseline

    TimeList = np.array(TimeList)
    AmpList = np.array(AmpList)

    for Index in range(BinSize):
        if Min > AmpList[Index]:
            Min = AmpList[Index]

    path1 = "/home/cz/readout/test3/0927/C3--XX--%05d.trc"% (eventIndex)
    data1 = lecroyparser.ScopeData(path1)
    amp1 = data1.y
    AmpList1 = amp1.tolist()
    baseline = 0
    indexnum = 0
    for index in range(len(TimeList)):
        AmpList1[index] = AmpList1[index] * 1000
        if TimeList[index] > 300 and TimeList[index] < 320:
            baseline += AmpList1[index]
            indexnum += 1
    baseline = baseline / indexnum
    for index in range(len(TimeList)):
         AmpList1[index] = AmpList1[index] - baseline

    for Index in range(BinSize):
        if Min1 > AmpList1[Index]:
            Min1 = AmpList1[Index]
    for i in range(RangeNum):
        if AmplitudeList[i] < Min < AmplitudeList[i+1]:
          Amplitude2HistList[i].Fill(Min1)
    #print("Min: ",Min,Min1)
    AmplitudeHist_2D.Fill(Min,Min1)

for i in range(RangeNum):
    print("Amplitude_mean: ",round(Amplitude2HistList[i].GetMean(),2))

c3 = TCanvas("c3", "BPRE", 800, 600)
c3.cd()
c3.Divide(1,1,0.008,0.007)
gPad.SetTopMargin(0.09)
gPad.SetBottomMargin(0.10)
gPad.SetLeftMargin(0.10)
gPad.SetRightMargin(0.12)
l z= TLegend(0.60, 0.62, 0.88, 0.87)
l.SetBorderSize(0)
l.SetFillStyle(0)
l.SetTextFont(42)
l.SetTextSize(0.026)

AmplitudeHist_2D.Draw("COLZ")
ax = AmplitudeHist_2D.GetXaxis()
ax.SetTitle( " Amplitude 1 (mV) " )
ay = AmplitudeHist_2D.GetYaxis()
ay.SetTitle( " Amplitude 2 (mV) " )
ay.SetTitleSize(0.04)
ax.SetTitleOffset(1.0)
ay.SetTitleOffset(1.2)
ax.SetTitleSize(0.04)
ax.SetLabelSize(0.04)
ay.SetLabelSize(0.04)
ax.Draw("same")
ay.Draw("same")
c3.SaveAs("Amplitude.png")

Amplitude2HistList[0] = Amplitude2HistList[0].DrawNormalized("H")
Amplitude2HistList[0].SetStats(0)
Amplitude2HistList[0].SetLineColor(1)
ax = Amplitude2HistList[0].GetXaxis()
ax.SetTitle( " Amplitude 2 (mV) " )
ay = Amplitude2HistList[0].GetYaxis()
ay.SetTitle( " Event " )
ay.SetTitleSize(0.04)
ax.SetTitleOffset(1.0)
ay.SetTitleOffset(1.2)
ax.SetTitleSize(0.04)
ax.SetLabelSize(0.04)
ay.SetLabelSize(0.04)
ax.Draw("same")
ay.Draw("same")
l.AddEntry(Amplitude2HistList[0], "Amp 1: {0}~{1} mV,Mean: {2} mV".format(AmplitudeList[0],AmplitudeList[1],round(Amplitude2HistList[0].GetMean(),2)), "l")
for i in range(1,RangeNum):
    Amplitude2HistList[i] = Amplitude2HistList[i].DrawNormalized("Hsame")
    Amplitude2HistList[i].SetLineColor(i+1)
    l.AddEntry(Amplitude2HistList[i], "Amp 1: {0}~{1} mV,Mean: {2} mV".format(AmplitudeList[i],AmplitudeList[i+1],round(Amplitude2HistList[i].GetMean(),2)), "l")
l.Draw("same")
c3.SaveAs("Amplitude_Dis.png")
