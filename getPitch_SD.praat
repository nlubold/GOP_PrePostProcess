# Intensity extractor
# Nichola Lubold 3/10/2015
 
form Multi Entrainment
	text directory D:\ASU\TBICorpus\Experiments\CombinedLabAudio\TB\tb28\PAR\
endform


Create Strings as file list... fileList 'directory$'*.wav


nFiles = Get number of strings

for d from 1 to nFiles

	select Strings fileList
    	fileName$ = Get string... d

	Read from file... 'directory$''fileName$'
	soundname$ = selected$("Sound")

	floor = 100
	ceiling = 500

	select Sound 'soundname$'

	To Pitch... 0.01 floor ceiling
	avgUser = Get mean... 0 0 Hertz
	sdUser = Get standard deviation... 0 0 Hertz
	
	printline 'directory$','soundname$','avgUser','sdUser'

	select Pitch 'soundname$'

	Remove

endfor

select all
Remove

