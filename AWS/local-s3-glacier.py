#! python
import sys
import os
import subprocess
import time
from datetime import datetime

##Author: David Prat
##Date 19-2-2018

def compress(today):
	vpOrig=["F:\\X", "F:\\Y", "F:\\Z"]
	vpDest=["G:\\X_"+today+".zip", "G:\\Y_"+today+".zip", "G:\\Z_"+today+".zip"] 
	vpList=["G:\\list_X_"+today+".txt", "G:\\list_Y_"+today+".txt", "G:\\list_Z_"+today+".txt"] 

	i=0
	while i<len(vpOrig):
		pOrig=vpOrig[i]
		pDest=vpDest[i]
		pList=vpList[i]
		
		order= "E:\Software\Rar.exe A"
		order2=" "+pDest+" "+pOrig
		start = time.time()
		result=subprocess.Popen(order + order2, shell=False).wait()
		end = time.time()

		print(end - start)
		
		order="E:\Software\Rar.exe l"
		order2=" "+pDest+" > "+pList

		print (order+order2)
		result=subprocess.Popen(order + order2, shell=True).wait()
		print (result)
		i=i+1
		
def send(today, gl):
	vpOrig=["F:\\X", "F:\\Y", "F:\\Z"]
	vpDest=["G:\\X_"+today+".zip", "G:\\Y_"+today+".zip", "G:\\Z_"+today+".zip"] 
	vpList=["G:\\list_X_"+today+".txt", "G:\\list_Y_"+today+".txt", "G:\\list_Z_"+today+".txt"] 

	if (gl==0):
		bucket="back1/back2"
		flag=""
		
	else:
		bucket="back1/gl.back2"
		flag="--storage-class STANDARD_IA"
		
	i=0
	
	while i<len(vpOrig):
		
		pOrig=vpOrig[i]
		pDest=vpDest[i]
		pList=vpList[i]
		
		start = time.time()
		command="aws s3 cp "+pDest+" s3://"+bucket+"/"+pOrig.split("\\")[len(pOrig.split("\\"))-1]+"/ "+flag
		result=subprocess.Popen(command, shell=True).wait()
		end = time.time()
		print(end - start)
		print (result)
		
		command="aws s3 cp "+pList+" s3://"+bucket+"/"+pOrig.split("\\")[len(pOrig.split("\\"))-1]+"/ "+flag
		result=subprocess.Popen(command, shell=True).wait()
		print (result)
		i=i+1

def eliminate(today):
	vpOrig=["F:\\X", "F:\\Y", "F:\\Z"]
	i=0
	while i<len(vpOrig):
		pOrig=vpOrig[i]
		
		pOrigName=pOrig.split("\\")[len(pOrig.split("\\"))-1]
		
		commandLs="aws s3 ls s3://back1/back2/"+pOrigName+"/"
		res=os.popen(commandLs).readlines()
		print(res)
		
		while len(res)>2:#each backup are two files
			vdates=[]

			print ("more than 1 backup")
			for date in res:
				vdate=date.split("_")
				date=vdate[len(vdate)-1]
				vdate=date.split(".")
				date=vdate[0]
				date=date.strip()
				dto = datetime.strptime(date, '%d-%m-%Y').date()
				vdates.append(dto)
				print (date)
		
			print (vdates)
			minim=min(vdates)
			print ("min is: "+str(minim.strftime('%d-%m-%Y')))
			commandRm="aws s3 rm s3://back1/back2/"+pOrigName+"/"+pOrigName+"_"+str(minim.strftime('%d-%m-%Y'))+".zip"
			print ("commandrm: "+str(commandRm))
			result=subprocess.Popen(commandRm, shell=True).wait()
			
			commandRm="aws s3 rm s3://back1/back2/"+pOrigName+"/list_"+pOrigName+"_"+str(minim.strftime('%d-%m-%Y'))+".txt"
			print ("commandrm: "+str(commandRm))
			result=subprocess.Popen(commandRm, shell=True).wait()
			
			res=os.popen(commandLs).readlines()	
		i=i+1
		
def eliminteInternalCompressions(today):
	vpDest=["G:\\X_"+today+".zip", "G:\\Y_"+today+".zip", "G:\\Z_"+today+".zip"] 
	vpList=["G:\\list_X_"+today+".txt", "G:\\list_Y_"+today+".txt", "G:\\list_Z_"+today+".txt"] 
	
	i=0
	while i<len(vpDest):
	
		pDest=vpDest[i]
		pList=vpList[i]
		print (pDest)
		commandRm="del " # del is for windows normal cmd
		result=subprocess.Popen(commandRm + pDest, shell=True).wait()
		print (result)
		result=subprocess.Popen(commandRm + pList, shell=True).wait()
		print (result)
		i=i+1
	
def main(argv):
	sys.stdout.write("hello from Python %s\n" % (sys.version,))
	today=time.strftime("%d-%m-%Y")
	todayDoW=time.strftime("%A")
	todayDoM=time.strftime("%m")
	print ("today is: "+today+" doW is: "+str(todayDoW)+" DoM is: "+str(todayDoM))
	##################################################################
	###############################WEEKLY############################
	#####################Compress####################################
	if(todayDoW=="Thursday"  ):
		print ("going to compress")
		compress(today)
	#####################Send to S3########################
	if(todayDoW=="Thursday" ):
		print ("going to send to s3")
		send(today, 0)
	#####################Eliminate Old##########################
	#eliminate(today)
	if(todayDoW=="Thursday"):
		print ("going to check s3 and to eliminate")
		eliminate(today)
	#################Eliminate Compressions from internal HDD#######################
	if(todayDoW=="Thursday"):
		print ("going to eliminate internal compressions")
		eliminteInternalCompressions(today)
	#######################################################################
	###########################MONTHLY####################################
	#####################Compress####################################
	if((todayDoM=="28" and todayDoW!="Thursday") ):
		print ("going to compress if needed (glacier policy)")
		compress(today)
	#####################Send to S3 IA/glacier########################
	if(todayDoM=="28" ):
		print ("going to send to s3 (bucket glacier policy)")
		send(today, 1)
	#####################Eliminate Old##########################
	if(todayDoM=="28"):
		print ("going to check glacier")
		#never eliminte from glacier
		#################Eliminate Compressions from internal HDD#######################
	if(todayDoM=="28" and todayDoW!="Thursday" ):
		print ("going to eliminate internal compressions")
		eliminteInternalCompressions(today)	
	
main("")