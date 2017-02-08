import os
import sys
import xml.sax.handler
import xml.sax
import codecs
import re
import time
import json

reload(sys)  
sys.setdefaultencoding('utf8')

releaseCounter = 0
		

			
			
if ( __name__ == "__main__"):
	
	trackslength = []
	#trackoffsets = []
	disclength = []
	prevcombinenum = ''
	trackcombinenum = ''
	partialtracktitle = ''
	tracktitle = []
	#alltracksnolast = 0
	discartist = ''
	disctitle = ''
	nexttitle = ''
	discyear = ''
	discgenre = ''
	formattedtrackslengths = []
	formattedtracktitles = []
	indexer = ''
	morethanonetitle = 0
	aftertrackframeoffset = 0
	genreleaseidname = ''
	genreleasenametoid = ''
	
	fo = codecs.open('releases.json','w',encoding='utf8')
	fl = codecs.open('parselog.txt','w',encoding='utf8')
	#fo = open('releases.json','w')
	
	trackframeoffset = re.compile("#[ \t]+Track[ \t]+frame[ \t]+offsets:")
	framematch = re.compile("#[ +\t+]+[0-9]+")
	framematchnos = re.compile("#[0-9]+")
	framedontmatch = re.compile("#[ +\t+]+[0-9]+[ +\t+\-\_+a-z+:+]+")
	disclengthmatch = re.compile("# +Disc +length: +[0-9]+")
	tracktitlematch = re.compile("TTITLE[0-9]+=.*")
	discartisttitle = re.compile("DTITLE=.*")
	discyearmatch = re.compile("DYEAR=.*")
	discgenrematch = re.compile("DGENRE=.*")
	artiststitlematch = re.compile(" \/ ")
	
	indir = 'D:/FreeDB/FreedbDump/'
	for root, dirs, filenames in os.walk(indir):
		for filename in filenames:
	#with open("65078809") as infile:
			if (os.stat(os.path.join(root, filename)).st_size == 0):
				continue
			with open(os.path.join(root, filename)) as infile:
				#print(filename)
				fl.write(os.path.join(root, filename) + '\n')
				genreleaseidname = os.path.basename(os.path.normpath(root))
				if (genreleaseidname == "blues"):
					genreleasenametoid = "0001"
				if (genreleaseidname == "classical"):
					genreleasenametoid = "0002"
				if (genreleaseidname == "country"):
					genreleasenametoid = "0003"
				if (genreleaseidname == "data"):
					genreleasenametoid = "0004"
				if (genreleaseidname == "folk"):
					genreleasenametoid = "0005"
				if (genreleaseidname == "jazz"):
					genreleasenametoid = "0006"
				if (genreleaseidname == "misc"):
					genreleasenametoid = "0007"
				if (genreleaseidname == "newage"):
					genreleasenametoid = "0008"
				if (genreleaseidname == "reggae"):
					genreleasenametoid = "0009"
				if (genreleaseidname == "rock"):
					genreleasenametoid = "0010"
				if (genreleaseidname == "soundtrack"):
					genreleasenametoid = "0011"
				for line in infile:
					if (trackframeoffset.match(line)):
						aftertrackframeoffset = 1
					if (aftertrackframeoffset == 1):
						if ((not framedontmatch.match(line)) and (framematch.match(line)) or (framematchnos.match(line))):
							trackslength.append(map(int, re.findall('\d+', line)))
						if (disclengthmatch.match(line)):
							disclength.append(map(int, re.findall('\d+', line)))
						if (tracktitlematch.match(line)):
							trackcombinenum = line.split("=")[0]
							if trackcombinenum == prevcombinenum:
								prevcombinenum = line.split("=")[0]
								partialtracktitle = tracktitle[-1]
								partialtracktitle = partialtracktitle.rstrip() + line.split("=")[1].rstrip()
								tracktitle[-1] = partialtracktitle
								continue
							if trackcombinenum != prevcombinenum:
								prevcombinenum = line.split("=")[0]
								tracktitle.append(line.split("=")[1])
								continue
						if (discartisttitle.match(line)):
							morethanonetitle += 1
							if (morethanonetitle == 1):
								discartist = line.split(" / ")[0].decode('iso-8859-1').encode("utf-8").rstrip()
								discartist = re.sub('DTITLE=', '', discartist)
								try: 
									disctitle = line.split(" / ")[1].decode('iso-8859-1').encode("utf-8").rstrip()
									if not disctitle:
										disctitle = discartist
								except:
									disctitle = discartist
							if (morethanonetitle > 1):
								nexttitle = line.decode('iso-8859-1').encode("utf-8").rstrip()
								nexttitle = re.sub('DTITLE=', '', nexttitle)
								disctitle += nexttitle.decode('iso-8859-1').encode("utf-8")
								nexttitle = ''
						if (discyearmatch.match(line)):
							discyear = line.split("=")[1]
						if (discgenrematch.match(line)):
							discgenre = line.split("=")[1]
				for idx, item in enumerate(trackslength[:-1]):
					currentframe = map(lambda x: float(x)/75, trackslength[idx])
					nextframe = map(lambda x: float(x)/75, trackslength[idx + 1])
					tracknumlength = [a - b for a, b in zip(nextframe, currentframe)]
					m, s = divmod(tracknumlength[0], 60)
					h, m = divmod(m, 60)
					if(h == 0):
						timeconv = "%d:%02d" % (m, s)
					else:
						timeconv = "%d:%02d:%02d" % (h, m, s)
					#currentframe = int(currentframe) / 75
					#nextframe = int(nextframe) / 75
					#fo.write("tracknumber {0}: length: {1}\n".format(idx + 1, '' .join(map(str, timeconv))))
					formattedtrackslengths.append(timeconv)
				for item in disclength:
					#'' .join(map(str, item))
					lasttrackoffset = map(lambda x: float(x)/75, trackslength[-1])
					lasttracklength = [a - b for a, b in zip(item, lasttrackoffset)]
					m, s = divmod(lasttracklength[0], 60)
					h, m = divmod(m, 60)
					if(h == 0):
						timeconv = "%d:%02d" % (m, s)
					else:
						timeconv = "%d:%02d:%02d" % (h, m, s)
					#fo.write("tracknumber {0}: length: {1}\n".format(len(trackslength), timeconv))
					formattedtrackslengths.append(timeconv)
				for item in tracktitle:
					#fo.write("Title: {0}".format(item))
					formattedtracktitles.append(item.decode('iso-8859-1').encode("utf-8").rstrip())
				fo.write('{"releaseid": ' + json.dumps(genreleasenametoid + filename.decode('iso-8859-1').encode("utf-8").lower().rstrip()) + ', ')
				fo.write('"l_artist_name": ' + json.dumps(discartist.decode('iso-8859-1').encode("utf-8").lower().rstrip()) + ', ')
				fo.write('"artist_name": ' + json.dumps(discartist.decode('iso-8859-1').encode("utf-8").rstrip()) + ', ')
				fo.write('"l_title": ' + json.dumps(disctitle.decode('iso-8859-1').encode("utf-8").lower().rstrip()) + ', ')
				fo.write('"title": ' + json.dumps(disctitle.decode('iso-8859-1').encode("utf-8").rstrip()) + ', ')
				fo.write('"year": ' + json.dumps(discyear.decode('iso-8859-1').encode("utf-8").rstrip()) + ', ')
				fo.write('"genre": ' + json.dumps(discgenre.decode('iso-8859-1').encode("utf-8").rstrip()) + ', ')
				fo.write('"tracklist": [')
				if (len(formattedtrackslengths) == 0):
					fo.write(']')
				if (len(formattedtrackslengths) > 0):
					for idx, item in enumerate(formattedtrackslengths):
						indexer = idx + 1
						fo.write('{"track_position": ' + json.dumps(str(indexer)) + ', "track_title": ' + json.dumps(formattedtracktitles[idx]) + ', "track_duration": ' + json.dumps(formattedtrackslengths[idx]))
						if (indexer == len(formattedtrackslengths)):
							fo.write('}]')
						else:
							fo.write('},')
				fo.write('}\n')
				indexer = ''
				trackslength = []
				disclength = []
				prevcombinenum = ''
				trackcombinenum = ''
				partialtracktitle = ''
				tracktitle = []
				discartist = ''
				disctitle = ''
				discyear = ''
				discgenre = ''
				formattedtrackslengths = []
				formattedtracktitles = []
				morethanonetitle = 0
				aftertrackframeoffset = 0
				infile.close()
	fo.close()
	fl.close()
