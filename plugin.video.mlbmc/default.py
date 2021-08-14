# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License.
# *  If not, write to the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html
# *
# *  2011/05/30
# *
# *  Thanks and credit to:
# *
# *  mlbviewer  http://sourceforge.net/projects/mlbviewer/  Most of the mlb.tv code was from this project.
# *
# *  Everyone from the fourm - http://fourm.xbmc.org
# *    giftie - for the colored text code :) thanks.
# *    theophile and the others from - http://forum.xbmc.org/showthread.php?t=97251


import urllib,urllib2,re,os,cookielib,datetime
import xbmcplugin,xbmcgui,xbmcaddon
try:
    import json
except:
    import simplejson as json
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP


__settings__ = xbmcaddon.Addon(id='plugin.video.mlbmc')
__language__ = __settings__.getLocalizedString
addon = xbmcaddon.Addon('plugin.video.mlbmc')
profile = xbmc.translatePath(addon.getAddonInfo('profile'))
home = __settings__.getAddonInfo('path')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
fanart = xbmc.translatePath( os.path.join( home, 'fanart.jpg' ) )
fanart1 = 'http://mlbmc-xbmc.googlecode.com/svn/icons/fanart1.jpg'
fanart2 = 'http://mlbmc-xbmc.googlecode.com/svn/icons/fanart2.jpg'
debug = __settings__.getSetting('debug')


if debug == "true":
    print '(((((((((( Version 0.0.1 ))))))))))'

SOAPCODES = {
    "1"    : "OK",
    "-1000": "Requested Media Not Found",
    "-1500": "Other Undocumented Error",
    "-2000": "Authentication Error",
    "-2500": "Blackout Error",
    "-3000": "Identity Error",
    "-3500": "Sign-on Restriction Error",
    "-4000": "System Error",
    }
TeamCodes = {
    '108': ('Los Angeles Angels', 'ana'),
    '109': ('Arizona Diamondbacks', 'ari'),
    '144': ('Atlanta Braves', 'atl'),
    '110': ('Baltimore Orioles', 'bal'),
    '111': ('Boston Red Sox', 'bos'),
    '112': ('Chicago Cubs', 'chc'),
    '113': ('Cincinnati Reds', 'cin'),
    '114': ('Cleveland Indians', 'cle'),
    '115': ('Colorado Rockies', 'col'),
    '145': ('Chicago White Sox', 'cws'),
    '116': ('Detroit Tigers', 'det'),
    '146': ('Florida Marlins', 'fla'),
    '117': ('Houston Astros', 'hou'),
    '118': ('Kansas City Royals', 'kc'),
    '119': ('Los Angeles Dodgers', 'la'),
    '158': ('Milwaukee Brewers', 'mil'),
    '142': ('Minnesota Twins', 'min'),
    '121': ('New York Mets', 'nym'),
    '147': ('New York Yankees', 'nyy'),
    '133': ('Oakland Athletics', 'oak'),
    '143': ('Philadelphia Phillies', 'phi'),
    '134': ('Pittsburgh Pirates', 'pit'),
    '135': ('San Diego Padres', 'sd'),
    '136': ('Seattle Mariners', 'sea'),
    '137': ('San Francisco Giants', 'sf'),
    '138': ('St. Louis Cardinals', 'stl'),
    '139': ('Tampa Bay Rays', 'tb'),
    '140': ('Texas Rangers', 'tex'),
    '141': ('Toronto Blue Jays', 'tor'),
    '120': ('Washington Nationals', 'was')
    }

def categories():
        addDir(__language__(30000),'',3,'http://mlbmc-xbmc.googlecode.com/svn/icons/mlb.tv.png')
        addPlaylist(__language__(30001),'http://mlb.mlb.com/video/play.jsp?tcid=mm_mlb_vid',12,'http://mlbmc-xbmc.googlecode.com/svn/icons/latestvid.png')
        addDir(__language__(30002),'',4,'http://mlbmc-xbmc.googlecode.com/svn/icons/tvideo.png')
        addDir(__language__(30003),'http://mlb.mlb.com/ws/search/MediaSearchService?mlbtax_key=fastcast&sort=desc&sort_type=date&hitsPerPage=200&src=vpp',1,'http://mlbmc-xbmc.googlecode.com/svn/icons/fc.png')
        addDir(__language__(30004),'http://mlb.mlb.com/ws/search/MediaSearchService?mlbtax_key=must_c&sort=desc&sort_type=date&hitsPerPage=200&src=vpp',1,'http://mlbmc-xbmc.googlecode.com/svn/icons/mc.png')
        addDir(__language__(30005),'http://mlb.mlb.com/ws/search/MediaSearchService?&sort=desc&sort_type=date&subject=MLBCOM_GAME_RECAP&hitsPerPage=60&src=vpp',1,'http://mlbmc-xbmc.googlecode.com/svn/icons/gamere.png')
        addDir(__language__(30006),'http://mlb.mlb.com/ws/search/MediaSearchService?mlbtax_key=mlb_network&sort=desc&sort_type=date&hitsPerPage=360&src=vpp',1,'http://mlbmc-xbmc.googlecode.com/svn/icons/mlbnet.png')
        addDir(__language__(30007),'http://mlb.mlb.com/ws/search/MediaSearchService?&sort=desc&sort_type=date&subject=MLBCOM_TOP_PLAY&hitsPerPage=60&src=vpp',1,'http://mlbmc-xbmc.googlecode.com/svn/icons/tp.png')
        addDir(__language__(30008),'http://gdx.mlb.com/components/game/mlb/'+dateStr.day[0]+'/media/highlights.xml',8,'http://mlbmc-xbmc.googlecode.com/svn/icons/realtime.png')
        addDir(__language__(30009),'http://mlb.mlb.com/video/play.jsp?topic_id=7759164',10,'http://mlbmc-xbmc.googlecode.com/svn/icons/bball.png')


def mlbTV():
        if __settings__.getSetting('email') != "":
            addGameDir(__language__(30010),'http://mlb.mlb.com/gdcross/components/game/mlb/'+dateStr.day[0]+'/master_scoreboard.json',6,'http://mlbmc-xbmc.googlecode.com/svn/icons/mlb.tv.png')
            addGameDir(__language__(30011),'http://mlb.mlb.com/gdcross/components/game/mlb/'+dateStr.day[1]+'/master_scoreboard.json',6,'http://mlbmc-xbmc.googlecode.com/svn/icons/mlb.tv.png')
            addGameDir(__language__(30012),'http://mlb.mlb.com/gdcross/components/game/mlb/'+dateStr.day[3]+'/master_scoreboard.json',6,'http://mlbmc-xbmc.googlecode.com/svn/icons/mlb.tv.png')
            addGameDir(__language__(30013),'http://mlb.mlb.com/gdcross/components/game/mlb/'+dateStr.day[2]+'/master_scoreboard.json',6,'http://mlbmc-xbmc.googlecode.com/svn/icons/mlb.tv.png')
            addGameDir(__language__(30014),'',11,'http://mlbmc-xbmc.googlecode.com/svn/icons/mlb.tv.png')
        else:
            xbmc.executebuiltin("XBMC.Notification("+__language__(30015)+","+__language__(30016)+",30000,"+icon+")")
            __settings__.openSettings()


def getTeams():
        teams = TeamCodes.values()
        for team in teams:
            name = team[0]
            url = team[1]
            addPlaylist(name,url,5,'http://mlbmc-xbmc.googlecode.com/svn/icons/tvideo.png')


def getRealtimeVideo(url):
        try:
            req = urllib2.Request(url)
            req.addheaders = [('Referer', 'http://mlb.mlb.com/index.jsp'),
                  ('Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0) Gecko/20100101 Firefox/4.0')]
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            soup = BeautifulStoneSoup(link)

            videos = soup.findAll('media')
            for video in videos:
                name = video.headline.string
                vidId = video['id']
                url = vidId[-3]+'/'+vidId[-2]+'/'+vidId[-1]+'/'+vidId
                duration = video.duration.string
                thumb = video.thumb.string
                addLink(name,'http://mlb.mlb.com/gen/multimedia/detail/'+url+'.xml',duration,2,thumb)
        except:
            pass
        addDir(__language__(30017),'http://gdx.mlb.com/components/game/mlb/'+dateStr.day[1]+'/media/highlights.xml',8,icon)


def getTeamVideo(url):
        url='http://mlb.mlb.com/gen/'+url+'/components/multimedia/topvideos.xml'
        req = urllib2.Request(url)
        req.addheaders = [('Referer', 'http://mlb.mlb.com'),
                ('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3')]
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        soup = BeautifulStoneSoup(link, convertEntities=BeautifulStoneSoup.XML_ENTITIES)
        videos = soup('item')
        playlist = xbmc.PlayList(1)
        playlist.clear()
        for video in videos:
            name = video('title')[0].string
            thumb = video('picture', attrs={'type' : "dam-raw-thumb"})[0]('url')[0].string
            if video('url', attrs={'speed' : "1200"}):
                url = video('url', attrs={'speed' : "1200"})[0].string
            elif video('url', attrs={'speed' : "1000"}):
                url = video('url', attrs={'speed' : "1000"})[0].string
            elif video('url', attrs={'speed' : "800"}):
                url = video('url', attrs={'speed' : "800"})[0].string
            duration = video('duration')[0].string
            desc = video('big_blurb')[0].string
            info = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumb)
            playlist.add(url, info)
        play=xbmc.Player().play(playlist)


def scrapeWebsite(url):
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        req.addheaders = [('Referer', 'http://mlb.mlb.com'),
                ('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3')]
        link=response.read()
        response.close()
        soup = BeautifulSoup(link, convertEntities=BeautifulSoup.HTML_ENTITIES)
        videos = soup.find('div', attrs={'id' : "playlistWrap"})('li')
        for video in videos:
            name = video('p')[0].string
            try:
                thumb = video('img')[0]['data-src']
            except:
                thumb = video('img')[0]['src']
            content = video('a')[0]['rel']
            url = content[-3]+'/'+content[-2]+'/'+content[-1]+'/'+content
            duration = video('div', attrs={'class' : "duration"})[0].string[-5:]
            addLink(name,'http://mlb.mlb.com/gen/multimedia/detail/'+url+'.xml',duration,2,thumb)


def playLatest(url):
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        req.addheaders = [('Referer', 'http://mlb.mlb.com'),
                ('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3')]
        link=response.read()
        response.close()
        soup = BeautifulSoup(link, convertEntities=BeautifulSoup.HTML_ENTITIES)
        videos = soup.find('div', attrs={'id' : "playlistWrap"})('li')
        playlist = xbmc.PlayList(1)
        playlist.clear()
        for video in videos:
            name = video('p')[0].string
            try:
                thumb = video('img')[0]['data-src']
            except:
                thumb = video('img')[0]['src']
            content = video('a')[0]['rel']
            url = content[-3]+'/'+content[-2]+'/'+content[-1]+'/'+content
            url = getVideoURL('http://mlb.mlb.com/gen/multimedia/detail/'+url+'.xml')
            info = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumb)
            playlist.add(url, info)
        play=xbmc.Player().play(playlist)


def getVideos(url):
        try:
            req = urllib2.Request(url)
            req.addheaders = [('Referer', 'http://mlb.mlb.com/video/play.jsp?cid=mlb'),
                    ('Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0) Gecko/20100101 Firefox/4.0')]
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
        except urllib2.URLError, e:
            errorStr = str(e.read())
            if debug == 'true':
                print 'We failed to open "%s".' % url
                if hasattr(e, 'reason'):
                    print 'We failed to reach a server.'
                    print 'Reason: ', e.reason
                if hasattr(e, 'code'):
                    print 'We failed with error code - %s.' % e.code
                xbmc.executebuiltin("XBMC.Notification("+__language__(30015)+","+__language__(30018)+errorStr+",10000,"+icon+")")
            else:
                xbmc.executebuiltin("XBMC.Notification("+__language__(30015)+","+__language__(30018)+errorStr+",10000,"+icon+")")
        data = json.loads(link)
        videos = data['mediaContent']
        for video in videos:
            name = video['blurb']
            desc = video['bigBlurb']
            url = video['url']
            thumb = video['thumbnails'][2]['src']
            addLink(name,url,'',2,thumb)


def setVideoURL(url):
        url = getVideoURL(url)
        item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)


def getVideoURL(url):
        req = urllib2.Request(url)
        req.addheaders = [('Referer', 'http://mlb.mlb.com/video/play.jsp?cid=mlb'),
                ('Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0) Gecko/20100101 Firefox/4.0')]
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        soup = BeautifulStoneSoup(link)
        if soup.find('url', attrs={'playback_scenario' : "FLASH_1200K_640X360"}):
            url = soup.find('url', attrs={'playback_scenario' : "FLASH_1200K_640X360"}).string
        elif soup.find('url', attrs={'playback_scenario' : "FLASH_1000K_640X360"}):
            url = soup.find('url', attrs={'playback_scenario' : "FLASH_1000K_640X360"}).string
        elif soup.find('url', attrs={'playback_scenario' : "FLASH_600K_400X224"}):
            url = soup.find('url', attrs={'playback_scenario' : "FLASH_600K_400X224"}).string
        return url


def getGames(url):
        req = urllib2.Request(url)
        req.addheaders = [('Referer', 'http://mlb.mlb.com/index.jsp'),
                        ('Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0) Gecko/20100101 Firefox/4.0')]
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        data = json.loads(link)
        games = data['data']['games']['game']
        for game in games:
            home_team = game['home_team_city']
            away_team = game['away_team_city']
            game_id = game['game_pk']
            status = game['status']['status']
            if status == 'ind' or status == 'Preview':
                status = str(game['time']) + ' ' + str(game['time_zone'])

            try:
                thumb = game['video_thumbnail']
            except:
                thumb = ''

            try:
                event_id = game['game_media']['media'][0]['calendar_event_id']
            except:
                try:
                    event_id = game['game_media']['media']['calendar_event_id']
                except:
                    event_id = ''

            try:
                content_id = game['game_media']['media'][1]['content_id']
            except:
                content_id = ''

            try:
                free_game = game['game_media']['media']['free']
                if free_game == 'ALL':
                    free = ' Free Game'
                else:
                    free = ''
            except:
                    free = ''

            try:
                media_state = game['game_media']['media']['media_state']
            except:
                try:
                    media_state = game['game_media']['media'][0]['media_state']
                except:
                    media_state = ''

            if status == 'In Progress':
                try:
                    desc = str(game['alerts']['text'])+' '+str(game['status']['inning_state'])+' '+str(game['status']['inning'])
                except:
                    desc = ''
                try:
                    inning = str(game['status']['inning_state'])+' '+str(game['status']['inning'])
                except:
                    inning = ''
            else:
                desc = ''
                inning = ''

            description = desc
            name = away_team+' @ '+home_team+' - '+status+' '+free
            u=sys.argv[0]+"?url=&mode=7&name="+urllib.quote_plus(name)+"&event="+urllib.quote_plus(event_id)+"&content="+urllib.quote_plus(content_id)
            if media_state == 'media_on':
                label1=coloring( name,"cyan",name )
                label2=coloring( inning,"orange",inning )
                liz=xbmcgui.ListItem( label1+' '+label2,iconImage="DefaultVideo.png", thumbnailImage=thumb)
                liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
            else:
                liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumb)
                liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
            liz.setProperty( "Fanart_Image", fanart1 )
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)


def mlbGame(event_id,content_id):
        if debug == "true":
            print '-----install opener'
        cj = cookielib.LWPCookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
        if debug == "true":
            print '-----get first cookie'
        # Get the cookie first
        theurl = 'https://secure.mlb.com/enterworkflow.do?flowId=registration.wizard&c_id=mlb'
        txheaders = {'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.13) Gecko/20080311 Firefox/2.0.0.13'}
        data = None
        req = urllib2.Request(theurl,data,txheaders)
        response = urllib2.urlopen(req)
        if debug == "true":
            print response
            print 'These are the cookies we have received so far :'
            for index, cookie in enumerate(cj):
                print index, '  :  ', cookie
            print '-------logging in'
        # now authenticate
        theurl = 'https://secure.mlb.com/authenticate.do'
        txheaders = {'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.13) Gecko/20080311 Firefox/2.0.0.13',
                     'Referer' : 'https://secure.mlb.com/enterworkflow.do?flowId=registration.wizard&c_id=mlb'}
        values = {'uri' : '/account/login_register.jsp',
                  'registrationAction' : 'identify',
                  'emailAddress' : __settings__.getSetting('email'),
                  'password' : __settings__.getSetting('password')}

        data = urllib.urlencode(values)
        try:
           req = urllib2.Request(theurl,data,txheaders)
           response = urllib2.urlopen(req)
        except IOError, e:
            print 'We failed to open "%s".' % theurl
            if hasattr(e, 'code'):
                print 'We failed with error code - %s.' % e.code
            elif hasattr(e, 'reason'):
                print "The error object has the following 'reason' attribute :", e.reason
                print "This usually means the server doesn't exist, is down, or we don't have an internet connection."
                xbmc.executebuiltin("XBMC.Notification("+__language__(30015)+","+__language__(30019)+",10000,"+icon+")")
                return

        if debug == "true":
            print 'Here are the headers of the page :'
            print response.info()                             # handle.read() returns the page, handle.geturl() returns the true url of the page fetched (in case urlopen has followed any redirects, which it sometimes does)

            if cj == None:
                print "We don't have a cookie library available - sorry."
                print "I can't show you any cookies."
            else:
                print 'These are the cookies we have received so far :'
                for index, cookie in enumerate(cj):
                    print index, '  :  ', cookie

        page = response.read()
        pattern = re.compile(r'Welcome to your personal (MLB|mlb).com account.')
        try:
            loggedin = re.search(pattern, page).groups()
            print "Logged in successfully!"
        except:
            xbmc.executebuiltin("XBMC.Notification("+__language__(30015)+","+__language__(30020)+",5000,"+icon+")")
            pass

        # Begin MORSEL extraction
        ns_headers = response.headers.getheaders("Set-Cookie")
        attrs_set = cookielib.parse_ns_headers(ns_headers)
        cookie_tuples = cookielib.CookieJar()._normalized_cookie_tuples(attrs_set)
        print repr(cookie_tuples)
        cookies = {}
        for tup in cookie_tuples:
            name, value, standard, rest = tup
            cookies[name] = value
        print repr(cookies)

        # End MORSEL extraction


        # pick up the session key morsel
        theurl = 'http://mlb.mlb.com/enterworkflow.do?flowId=media.media'
        txheaders = {'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.13) Gecko/20080311 Firefox/2.0.0.13'}
        data = None
        req = urllib2.Request(theurl,data,txheaders)
        response = urllib2.urlopen(req)

        # Begin MORSEL extraction
        ns_headers = response.headers.getheaders("Set-Cookie")
        attrs_set = cookielib.parse_ns_headers(ns_headers)
        cookie_tuples = cookielib.CookieJar()._normalized_cookie_tuples(attrs_set)
        print repr(cookie_tuples)
        for tup in cookie_tuples:
            name, value, standard, rest = tup
            cookies[name] = value

        try:
            print "session-key = " + str(cookies['ftmu'])
            session_key = urllib.unquote(cookies['ftmu'])

        except:
            session_key = None
            logout_url = 'https://secure.mlb.com/enterworkflow.do?flowId=registration.logout&c_id=mlb'
            txheaders = {'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.13) Gecko/20080311 Firefox/2.0.0.13',
                     'Referer' : 'http://mlb.mlb.com/index.jsp'}
            data = None
            req = urllib2.Request(logout_url,data,txheaders)
            response = urllib2.urlopen(req)
            logout_info = response.read()
            response.close()
            if debug == "true":
                print "No session key, so logged out."

        try:
            values = {
                'eventId': event_id,
                'sessionKey': session_key,
                'fingerprint': urllib.unquote(cookies['fprt']),
                'identityPointId': cookies['ipid'],
                'subject':'LIVE_EVENT_COVERAGE'
            }
        except:
            xbmc.executebuiltin("XBMC.Notification("+__language__(30015)+","+__language__(30021)+",10000,"+icon+")")

        theUrl = 'https://secure.mlb.com/pubajaxws/bamrest/MediaService2_0/op-findUserVerifiedEvent/v-2.1?' +\
            urllib.urlencode(values)
        req = urllib2.Request(theUrl, None, txheaders);
        response = urllib2.urlopen(req).read()
        if debug == "true":
            print response

        soup = BeautifulSOAP(response)
        status = soup.find('status-code').string
        if status != "1":
            error_str = SOAPCODES[status]
            xbmc.executebuiltin("XBMC.Notification("+__language__(30015)+","+__language__(30022)+error_str+",10000,"+icon+")")
            return

        items = soup.findAll('user-verified-content', attrs={'type' : 'video'})
        try:
            session = soup.find('session-key').string
        except:
            session = ''
        event_id = soup.find('event-id').string
        for item in items:
            if soup.find('state').string == 'MEDIA_ARCHIVE':
                scenario = __settings__.getSetting('archive_scenario')
            else:
                scenario = __settings__.getSetting('scenario')
            content_id = item('content-id')[0].string
            blackout_status = item('blackout-status')[0].string
            try:
                blackout = item('blackout')[0].string.replace('_',' ')
            except:
                blackout = ''
            call_letters = item('domain-attribute', attrs={'name' : "call_letters"})[0].string
            if item('domain-attribute', attrs={'name' : "home_team_id"})[0].string == item('domain-attribute', attrs={'name' : "coverage_association"})[0].string:
                coverage = TeamCodes[item('domain-attribute', attrs={'name' : "home_team_id"})[0].string][0]+' Coverage'
            elif item('domain-attribute', attrs={'name' : "away_team_id"})[0].string == item('domain-attribute', attrs={'name' : "coverage_association"})[0].string:
                coverage = TeamCodes[item('domain-attribute', attrs={'name' : "away_team_id"})[0].string][0]+' Coverage'
            else:
                coverage = ''
            if blackout_status == '<successstatus></successstatus>':
                name = coverage+' - '+call_letters
            else:
                name = coverage+' '+call_letters+' '+blackout

            if item.state.string == 'MEDIA_OFF':
                try:
                    preview = soup.find('preview-url').contents[0]
                    if re.search('innings-index',str(preview)):
                        if debug == "true":
                            print '------> research'
                            print preview
                        raise Exception
                    else:
                        name = 'Preview Video - '+name
                        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
                        liz.setInfo( type="Video", infoLabels={ "Title": name } )
                        liz.setProperty( "Fanart_Image", fanart1 )
                        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=preview,listitem=liz)
                except:
                    pass
            else:
                u=sys.argv[0]+"?url=&mode=9&name="+urllib.quote_plus(name)+"&event="+urllib.quote_plus(event_id)+"&content="+urllib.quote_plus(content_id)+"&session="+urllib.quote_plus(session)+"&cookieIp="+urllib.quote_plus(cookies['ipid'])+"&cookieFp="+urllib.quote_plus(cookies['fprt'])+"&scenario="+urllib.quote_plus(scenario)
                if blackout_status == '<successstatus></successstatus>':
                    label1=coloring( name,"cyan",name )
                    liz=xbmcgui.ListItem( label1,iconImage="DefaultVideo.png")
                    liz.setInfo( type="Video", infoLabels={ "Title": name } )
                else:
                    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
                    liz.setInfo( type="Video", infoLabels={ "Title": name } )
                liz.setProperty( "Fanart_Image", fanart1 )
                liz.setProperty('IsPlayable', 'true')
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)


def getGameURL(name,event,content,session,cookieIp,cookieFp):
        if debug == "true":
            print "Event-id = " + str(event) + " content-id = " + str(content) + " Name = " + name + " Session = " + session + " cookieIp = " + cookieIp + " cookieFp = " + cookieFp + " scenario = " + scenario
        txheaders = {'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.13) Gecko/20080311 Firefox/2.0.0.13'}
        values = {
            'subject':'LIVE_EVENT_COVERAGE',
            'sessionKey': session,
            'identityPointId': cookieIp,
            'contentId': content,
            'playbackScenario': scenario,
            'eventId': event,
            'fingerprint': cookieFp,
        }
        theUrl = 'https://secure.mlb.com/pubajaxws/bamrest/MediaService2_0/op-findUserVerifiedEvent/v-2.1?' +\
            urllib.urlencode(values)
        req = urllib2.Request(theUrl, None, txheaders);
        response = urllib2.urlopen(req).read()
        if debug == "true":
            print response
        soup = BeautifulStoneSoup(response, convertEntities=BeautifulStoneSoup.XML_ENTITIES)
        status = soup.find('status-code').string

        if status != "1":
            error_str = SOAPCODES[status]
            xbmc.executebuiltin("XBMC.Notification("+__language__(30015)+","+__language__(30022)+error_str+",10000,"+icon+")")
            return

        elif soup.find('state').string == 'MEDIA_OFF':
            print 'Status : Media Off'
            try:
                preview = soup.find('preview-url').contents[0]
                if re.search('innings-index',str(preview)):
                    if debug == "true":
                        print '------> research'
                        print preview
                    raise Exception
                else:
                    xbmc.executebuiltin("XBMC.Notification("+__language__(30015)+","+__language__(30023)+",15000,"+icon+")")
                    item = xbmcgui.ListItem(path=preview)
                    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
            except:
                xbmc.executebuiltin("XBMC.Notification("+__language__(30015)+","+__language__(30023)+",5000,"+icon+")")
                return


        elif str(soup.find('blackout-status').next) != '<successstatus></successstatus>':
            try:
                blackout = item('blackout')[0].string.replace('_',' ')
            except:
                blackout = 'Blackout'
            try:
                preview = soup.find('preview-url').contents[0]
                if re.search('innings-index',str(preview)):
                    if debug == "true":
                        print '------> research'
                        print preview
                    raise Exception
                else:
                    xbmc.executebuiltin("XBMC.Notification("+__language__(30015)+","+__language__(30022)+blackout+__language__(30024)+",15000,"+icon+")")
                    item = xbmcgui.ListItem(path=preview)
                    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
            except:

                xbmc.executebuiltin("XBMC.Notification("+__language__(30015)+","+__language__(30022)+blackout+__language__(30024)+",5000,"+icon+")")
                return

        elif str(soup.find('auth-status').next) == '<notauthorizedstatus></notauthorizedstatus>':
            print 'Status : Not Authorized'
            try:
                preview = soup.find('preview-url').contents[0]
                if re.search('innings-index',str(preview)):
                    if debug == "true":
                        print '------> research'
                        print preview
                    raise Exception
                else:
                    xbmc.executebuiltin("XBMC.Notification("+__language__(30015)+","+__language__(30025)+",15000,"+icon+")")
                    item = xbmcgui.ListItem(path=preview)
                    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
            except:
                xbmc.executebuiltin("XBMC.Notification("+__language__(30015)+","+__language__(30026)+",5000,"+icon+")")
                return

        else:
            try:
                game_url = soup.findAll('user-verified-content')[0]('user-verified-media-item')[0]('url')[0].string
                if debug == "true":
                    print '-----> game_url = '+game_url
            except:
                if debug == "true":
                    print '-----------------> divingmule needs to work on the soup!'
                    print soup
                xbmc.executebuiltin("XBMC.Notification("+__language__(30015)+","+__language__(30027)+",5000,"+icon+")")

            if re.search('ondemand', game_url):
                play_path_pat = re.compile(r'ondemand\/(.*)$')
                play_path = re.search(play_path_pat,game_url).groups()[0]
                app = ' app=ondemand?_fcs_vhost=cp65670.edgefcs.net&akmfv=1.6'
                app += game_url.split('?')[1]
                swfurl = ' swfUrl="http://mlb.mlb.com/flash/mediaplayer/v4.2/R6/MediaPlayer4.swf?v=15'
                url = str(game_url)+swfurl+' playpath='+str(play_path)+app
                print '-----------ondemand-url = '+url
                item = xbmcgui.ListItem(path=url)
                xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

            elif re.search('live/',game_url):
                rtmp = game_url.split('mlb_')[0]
                play_path = ' playpath=mlb_'+game_url.split('mlb_')[1]
                pageurl = ' pageUrl="http://mlb.mlb.com/flash/mediaplayer/v4.2/R6/MP4.jsp?calendar_event_id='+soup.find('event-id').string+'&content_id=&media_id=&view_key=&media_type=video&source=MLB&sponsor=MLB&clickOrigin=&affiliateId=&team=mlb&"'
                swfurl = ' swfUrl="http://mlb.mlb.com/flash/mediaplayer/v4.2/R6/MediaPlayer4.swf?v=15'
                url = rtmp[:-1]+swfurl+pageurl+play_path+' live=1'
            if debug == "true":
                print 'mlbGame URL----> '+url
            item = xbmcgui.ListItem(path=url)
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)


def getDate():
        date = ''
        keyboard = xbmc.Keyboard(date, 'Format: yyyy/mm/dd' )
        keyboard.doModal()
        if (keyboard.isConfirmed() == False):
            return
        date = keyboard.getText()
        if len(date) != 10:
            xbmc.executebuiltin("XBMC.Notification("+__language__(30015)+","+__language__(30028)+errorStr+",5000,"+icon+")")
            return
        date = 'year_'+date.split('/')[0]+'/month_'+date.split('/')[1]+'/day_'+date.split('/')[2]
        url = 'http://mlb.mlb.com/gdcross/components/game/mlb/'+date+'/master_scoreboard.json'
        try:
            getGames(url)
        except urllib2.URLError, e:
            errorStr = str(e.read())
            if debug == 'true':
                print 'We failed to open "%s".' % url
                if hasattr(e, 'reason'):
                    print 'We failed to reach a server.'
                    print 'Reason: ', e.reason
                if hasattr(e, 'code'):
                    print 'We failed with error code - %s.' % e.code
                xbmc.executebuiltin("XBMC.Notification("+__language__(30015)+","+__language__(30018)+errorStr+"',10000,"+icon+")")
            else:
                xbmc.executebuiltin("XBMC.Notification("+__language__(30015)+","+__language__(30018)+errorStr+"',10000,"+icon+")")


class dateStr:
        today = datetime.date.today()
        ty = 'year_'+str(today).split()[0].split('-')[0]
        tm = '/month_'+str(today).split()[0].split('-')[1]
        tday = '/day_'+str(today).split()[0].split('-')[2]
        t = ty+tm+tday

        one_day = datetime.timedelta(days=1)

        yesterday = today - one_day
        yy = 'year_'+str(yesterday).split()[0].split('-')[0]
        ym = '/month_'+str(yesterday).split()[0].split('-')[1]
        yday = '/day_'+str(yesterday).split()[0].split('-')[2]
        y = yy+ym+yday

        tomorrow = today + one_day
        toy = 'year_'+str(tomorrow).split()[0].split('-')[0]
        tom = '/month_'+str(tomorrow).split()[0].split('-')[1]
        tod = '/day_'+str(tomorrow).split()[0].split('-')[2]
        to = toy+tom+tod

        byesterday = yesterday - one_day
        byy = 'year_'+str(byesterday).split()[0].split('-')[0]
        bym = '/month_'+str(byesterday).split()[0].split('-')[1]
        byday = '/day_'+str(byesterday).split()[0].split('-')[2]
        by = byy+bym+byday

        day = (t,y,to,by)


def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
            params=sys.argv[2]
            cleanedparams=params.replace('?','')
            if (params[len(params)-1]=='/'):
                params=params[0:len(params)-2]
            pairsofparams=cleanedparams.split('&')
            param={}
            for i in range(len(pairsofparams)):
                splitparams={}
                splitparams=pairsofparams[i].split('=')
                if (len(splitparams))==2:
                    param[splitparams[0]]=splitparams[1]

        return param


def coloring( text , color , colorword ):
        if color == "white":
            color="FFFFFFFF"
        if color == "blue":
            color="FF0000FF"
        if color == "cyan":
            color="FF00B7EB"
        if color == "violet":
            color="FFEE82EE"
        if color == "pink":
            color="FFFF1493"
        if color == "red":
            color="FFFF0000"
        if color == "green":
            color="FF00FF00"
        if color == "yellow":
            color="FFFFFF00"
        if color == "orange":
            color="FFFF4500"
        colored_text = text.replace( colorword , "[COLOR=%s]%s[/COLOR]" % ( color , colorword ) )
        return colored_text


def addLink(name,url,duration,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "duration": duration } )
        liz.setProperty('IsPlayable', 'true')
        liz.setProperty( "Fanart_Image", fanart2 )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


def addGameDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanart2 )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


def addPlaylist(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok


params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:
        event=urllib.unquote_plus(params["event"])
except:
        pass
try:
        content=urllib.unquote_plus(params["content"])
except:
        pass
try:
        session=urllib.unquote_plus(params["session"])
except:
        pass
try:
        cookieIp=urllib.unquote_plus(params["cookieIp"])
except:
        pass
try:
        cookieFp=urllib.unquote_plus(params["cookieFp"])
except:
        pass

try:
        scenario=urllib.unquote_plus(params["scenario"])
except:
        pass



print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None:
        print ""
        categories()

if mode==1:
        print""
        getVideos(url)

if mode==2:
        print""
        setVideoURL(url)

if mode==3:
        print""
        mlbTV()

if mode==4:
        print""
        getTeams()

if mode==5:
        print""		
        getTeamVideo(url)

if mode==6:
        print""		
        getGames(url)

if mode==7:
        print""		
        mlbGame(event,content)

if mode==8:
        print""		
        getRealtimeVideo(url)

if mode==9:
        print""		
        getGameURL(name,event,content,session,cookieIp,cookieFp)

if mode==10:
        print""
        scrapeWebsite(url)

if mode==11:
        print""
        getDate()

if mode==12:
        print""
        playLatest(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
