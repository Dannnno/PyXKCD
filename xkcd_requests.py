"""
Copyright (c) 2014 Dan Obermiller

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

You should have received a copy of the MIT License along with this program.
If not, see <http://opensource.org/licenses/MIT>
"""

import datetime
import json
import requests
import shutil
import subprocess

# Sample json format of comic 614
#
# {
#  "day": "24",
#  "month": "7",
#  "year": "2009", 
#  "num": 614, 
#  "link": "",  
#  "news": "", 
#  "safe_title": "Woodpecker", 
#  "transcript": "[[A man with a beret and a woman are standing on a boardwalk, leaning on a handrail.]]\nMan: A woodpecker!\n<<Pop pop pop>>\nWoman: Yup.\n\n[[The woodpecker is banging its head against a tree.]]\nWoman: He hatched about this time last year.\n<<Pop pop pop pop>>\n\n[[The woman walks away.  The man is still standing at the handrail.]]\n\nMan: ... woodpecker?\nMan: It's your birthday!\n\nMan: Did you know?\n\nMan: Did... did nobody tell you?\n\n[[The man stands, looking.]]\n\n[[The man walks away.]]\n\n[[There is a tree.]]\n\n[[The man approaches the tree with a present in a box, tied up with ribbon.]]\n\n[[The man sets the present down at the base of the tree and looks up.]]\n\n[[The man walks away.]]\n\n[[The present is sitting at the bottom of the tree.]]\n\n[[The woodpecker looks down at the present.]]\n\n[[The woodpecker sits on the present.]]\n\n[[The woodpecker pulls on the ribbon tying the present closed.]]\n\n((full width panel))\n[[The woodpecker is flying, with an electric drill dangling from its feet, held by the cord.]]\n\n{{Title text: If you don't have an extension cord I can get that too.  Because we're friends!  Right?}}", 
#  "alt": "If you don't have an extension cord I can get that too.  Because we're friends!  Right?", 
#  "img": "http:\/\/imgs.xkcd.com\/comics\/woodpecker.png", 
#  "title": "Woodpecker"
# }


class Comic(object):
    
    def __init__(self, image, title, number, date, alt, **kwargs):
        self.image = image
        self.url = ''.join(['http://www.xkcd.com/', str(number)])
        self.title = title
        self.comic_number = number
        self.date = datetime.datetime.strptime(date, '%Y/%m/%d')
        self.alt_text = alt
        
        ## Keyword values
        self.transcript = None
        self.link = None
        self.safe_title = title
        self.news = None
        for key, value in kwargs.iteritems():
            self.__dict__[key] = value
        self.safe_title = self.safe_title.replace(' ', '_')
            
    def display_comic(self):
        image = requests.get(self.image, stream=True)
        with open(''.join([
                            self.safe_title,
                            '.png'
                           ]), 'wb') as out_file:
            shutil.copyfileobj(image.raw, out_file)
        del image
        subprocess.check_call(self.safe_title+'.png', shell=True)
        print self
        print "Alt text:", self.alt_text
            
    def __str__(self):
        if self.transcript is not None:
            return self.transcript
        return "Comic number {}: {}".format(self.comic_number, self.title)
        
    def __repr__(self): return str(self)
    
    def __unicode__(self): return unicode(str(self))


class What_If(object):
    
    def __init__(self):
        raise NotImplementedError
        
    
class Explain_Comic(object):
    
    def __init__(self):
        raise NotImplementedError


def get_newest_comic():
    return get_comic_num()

    
def get_comic_num(num=None):
    if num is None:
        url = "http://xkcd.com/info.0.json"
    else: 
        url = "http://xkcd.com/{}/info.0.json".format(num)
    r = requests.get(url)
    return json.loads(r.text, object_hook=json_to_comic)
        
        
def get_what_if(num):
    url = "what-if.xkcd.com/{}/".format(num)
    return url
    
    
def get_explain_xkcd(num):
    url = "http://www.explainxkcd.com/wiki/index.php/{}".format(num)
    return url

    
def parse_transcript(transcript): 
    lines = transcript.split('\n')
    transcript = {}
    for line in lines:
        if line:
            if line.startswith('[[') and line.endswith(']]'):
                print 'Description', line[2:-2]
            elif line.startswith('{{') and line.endswith('}}'):
                print line[2:-2]
            else:
                print 'Spoken words', line


def json_to_comic(d):
    image, title, number, year, month, day, alt_text = \
              map(d.pop, ['img', 'title', 'num', 'year', 'month', 'day', 'alt'])
    
    return Comic(
                  image, title, number, '/'.join([year, month, day]), alt_text,
                  **{key:value for key, value in d.iteritems() if value}
                 )          

if __name__ == "__main__":
    newest = get_newest_comic()
    newest.display_comic()