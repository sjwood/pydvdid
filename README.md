# pydvdid

[![Travis][1]][2]
[![Coveralls][3]][4]
[![Scrutinizer][5]][6]

## Overview

[pydvdid][7] is a pure Python implementation of the Windows API [IDvdInfo2::GetDiscID][8] method, as used by Windows Media Center to compute a 'practically unique' 64-bit [CRC][9] for metadata retrieval. 

## Motivation

I needed a zero-knowledge way to recover some basic information about an inserted DVD or a mounted ISO image, and whilst googling ran across [dvdid][10]. A compiled solution didn't fit with my requirement, so I re-implemented it as a Python module. Kudos go to Christopher Key for originally developing dvdid and documenting the algorithm so thoroughly.

pydvdid is envisaged to be useful for DVD ripping scripts, custom Growl notifications, and media centre related home automation tasks.

## Compatibility

Works for Python versions 2 and 3, from 2.6 through to the nightly build.

## Availability

Get it from [PyPI][12] or directly from GitHub.

#### PyPI:

[![PyPI status][11]][12]
[![PyPI version][13]][12]
[![PyPI format][14]][12]
[![PyPI python versions][15]][12]

```sh
pip install pydvdid
```

#### GitHub:

[Releases][16]

## Examples

#### From the shell:

```sh
steve@babbage:~$ crc64=$(pydvdid /mnt/dvd)
steve@babbage:~$ echo $crc64
6e23e6a41a154405
steve@babbage:~$ curl --get http://metaservices.windowsmedia.com/pas_dvd_B/template/GetMDRDVDByCRC.xml?CRC=$crc64
<?xml version='1.0' encoding="UTF-8" ?><METADATA xmlns:sql="urn:schemas-microsoft-com:xml-sql">
	
	<MDR-DVD><version>4.0</version><dvdTitle>LEGO Star Wars: The Padawan Menace [French] [Blu-ray/DVD]</dvdTitle><studio>20th Century Fox Home Entertainment (Canadian</studio><leadPerformer></leadPerformer><actors></actors><director></director><MPAARating></MPAARating><releaseDate>2012 02 07</releaseDate><genre>Science Fiction</genre><dataProvider>AMG</dataProvider><wmid_dvd>7DDE9379-18E0-446A-8214-BCD3D573A54A</wmid_dvd><dv_id>E   278184          </dv_id><dataProviderParams>Provider=AMG</dataProviderParams><dataProviderLogo>Provider=AMG</dataProviderLogo><moreInfoParams></moreInfoParams><title><titleNum>1</titleNum><titleTitle>LEGO Star Wars: The Padawan Menace [French] [Blu-ray/DVD]</titleTitle><studio>20th Century Fox Home Entertainment (Canadian</studio><director></director><leadPerformer></leadPerformer><actors></actors><MPAARating></MPAARating><genre>Science Fiction</genre><providerRating></providerRating><communityRating></communityRating></title></MDR-DVD>
</METADATA>
```

#### From Python:

pydvdid has a decidely simple API, with the important bits imported into the package level so they can be conveniently imported directly from the package.

```sh
>>> from pydvdid import compute
>>> crc64 = compute("/mnt/dvd")
>>> str(crc64)
'a5acf20f2e56954b'
>>> from urllib import urlopen
>>> urlopen("http://metaservices.windowsmedia.com/pas_dvd_B/template/GetMDRDVDByCRC.xml?CRC={0}".format(crc64)).read()
'<?xml version=\'1.0\' encoding="UTF-8" ?><METADATA xmlns:sql="urn:schemas-microsoft-com:xml-sql">\r\n\t\r\n\t<MDR-DVD><version>4.0</version><dvdTitle>Room on the Broom</dvdTitle><studio>N Circle Entertainment</studio><leadPerformer>Gillian Anderson; Rob Brydon; Martin Clunes; Sally Hawkins; Simon Pegg; Timothy Spall</leadPerformer><actors>Gillian Anderson; Rob Brydon; Martin Clunes; Sally Hawkins; Simon Pegg; Timothy Spall</actors><director>Jan Lachauer; Max Lang</director><MPAARating></MPAARating><releaseDate>2013 08 06</releaseDate><genre>Children&apos;s/Family</genre><largeCoverParams>cov150/drv600/v691/v69118k4p4h.jpg</largeCoverParams><smallCoverParams>cov075/drv600/v691/v69118k4p4h.jpg</smallCoverParams><dataProvider>AMG</dataProvider><wmid_dvd>E568D84B-4CB8-4296-8896-716DDCFA1458</wmid_dvd><dv_id>E   303360          </dv_id><dataProviderParams>Provider=AMG</dataProviderParams><dataProviderLogo>Provider=AMG</dataProviderLogo><moreInfoParams></moreInfoParams><title><titleNum>1</titleNum><titleTitle>Room on the Broom</titleTitle><studio>N Circle Entertainment</studio><director>Jan Lachauer; Max Lang</director><leadPerformer>Gillian Anderson; Rob Brydon; Martin Clunes; Sally Hawkins; Simon Pegg; Timothy Spall</leadPerformer><actors>Gillian Anderson; Rob Brydon; Martin Clunes; Sally Hawkins; Simon Pegg; Timothy Spall</actors><MPAARating></MPAARating><genre>Children&apos;s/Family</genre><providerRating></providerRating><communityRating></communityRating><chapter><chapterNum>1</chapterNum><chapterTitle>Scene One [4:47]</chapterTitle></chapter><chapter><chapterNum>2</chapterNum><chapterTitle>Scene Two [7:29]</chapterTitle></chapter><chapter><chapterNum>3</chapterNum><chapterTitle>Scene Three [4:31]</chapterTitle></chapter><chapter><chapterNum>4</chapterNum><chapterTitle>Scene Four [9:55]</chapterTitle></chapter></title></MDR-DVD>\r\n</METADATA>'
```

## License

[Apache License, Version 2.0][17]

  [1]: https://img.shields.io/travis/sjwood/pydvdid.svg
  [2]: https://travis-ci.org/sjwood/pydvdid
  [3]: https://img.shields.io/coveralls/sjwood/pydvdid.svg
  [4]: https://coveralls.io/r/sjwood/pydvdid
  [5]: https://img.shields.io/scrutinizer/g/sjwood/pydvdid.svg
  [6]: https://scrutinizer-ci.com/g/sjwood/pydvdid
  [7]: https://github.com/sjwood/pydvdid
  [8]: https://msdn.microsoft.com/en-us/library/windows/desktop/dd376453.aspx
  [9]: https://en.wikipedia.org/wiki/Cyclic_redundancy_check
  [10]: http://dvdid.cjkey.org.uk/
  [11]: https://img.shields.io/pypi/status/pydvdid.svg
  [12]: https://pypi.python.org/pypi/pydvdid
  [13]: https://img.shields.io/pypi/v/pydvdid.svg
  [14]: https://img.shields.io/pypi/format/pydvdid.svg
  [15]: https://img.shields.io/pypi/pyversions/pydvdid.svg
  [16]: https://github.com/sjwood/pydvdid/releases
  [17]: https://raw.githubusercontent.com/sjwood/pydvdid/master/LICENSE
