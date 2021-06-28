from bs4 import BeautifulSoup
import html5lib
import urllib
import difflib
import os
import traceback
import gzip 
import Utils as u


class Entry:
    globalRunID=None
    Parser=None

    def __init__(self):
        self.fields = {}
        self.debug=False
        self.dinfo=False
        self.dinfo_text=""


    def get(self, field):
        if field in self.fields:
            return self.fields[field]


            
        return None



    def set(self, field, value):
        self.fields.set(field, value)


    def createFileName(self):

        if (self.get('filename_base')):
            return self.get('filename_base')

        file = self.url
        file = file.replace("http://", "")
        file = file.replace("https://", "")
        file = file.replace("/", "_")
        file = file.replace("?", "_")
        file = file.replace("&", "_")


        return file


    
    def get_page(self, DOWNLOAD_DIR):
        op_file = DOWNLOAD_DIR + "/" + self.createFileName()


        UAs = dict({
          'ffox5': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12'
          })

        ua = UAs.get('ffox5') # TODO: 
    

        url = str(self.url).rstrip('\"')
        print("url:" + url)
    
        try:
            opener = urllib.request.build_opener()
        except urllib.error.HTTPError as e:
            print(f"Failed to open url {url}")
            return
    
        try:
            opener.addheaders = [('User-agent', ua)]
            req = opener.open(url, timeout=30)
    
            CHUNK = 16 * 1024
            with open(op_file, 'wb') as fp:
              while True:
                chunk = req.read(CHUNK)
                if not chunk: break

                fp.write(chunk)
    
        except urllib.error.HTTPError as e:
            print(e.fp.read())
    
        except urllib.error.URLError as e:
            if isinstance(e.reason, socket.timeout):
                print("Connection timedout - error: %r" % e)
            else:

                print("URL Error")
    
        except:
            print("ERROR: in get_page:" + traceback.format_exc())
    
        try:
            self.check_file_not_gzipped(op_file)
        except:
            print("ERROR: in get_page - failed gzip checking - " + traceback.format_exc())
    


    def get_subtree_from_html(self, file, html, tag, attribute_name, attribute_value):
        value = None

        entry_key = tag + "_" + attribute_name

        search = "<" + tag + " " + attribute_name + "='" + attribute_value + "'>"
        search_text = "&lt;" + tag + " " + attribute_name + "='" + attribute_value + "'&gt;"

        print("Getting content from root " + search + " tag")

        try:
            attrs=dict()
            attrs[attribute_name]=attribute_value

            print("main = html.find_all(" + tag + ",  attrs={" + attribute_name + " : " + attribute_value + "})")
            main = html.find_all(tag, attrs)

            if (len(main) > 0):
                self.dinfo_text = self.dinfo_text + "MATCHED " + str(len(main)) + " element(s) for root '" + search_text + "' tag <br>\n"
            print("MATCHED " + str(len(main)) + " element(s) for root '" + search + "' tag <br>\n")

            if (len(main) > 1):
                print("WARN: matched on more than 1 " + search + " tag")

            if (len(main) == 0):
                raise Exception("Not", " found")

            contents=main[0].contents 

            if self.debug:
                file = file + "." + entry_key + ".selection"
                print("Writing selection file: " + file)
                u.writeFile(file, str(contents))

            return contents

        except:

            print("ERROR: Failed to find root at " + search + " tag")
            if self.debug:
                print(traceback.format_exc())
                self.dinfo_text = self.dinfo_text + traceback.format_exc() + "<br>\n"
            raise


    
    def parse_page(self, DIR):

        url = self.get('url')
        print("--->parse_page(" + str(url) + ")")
        file = DIR + "/" + self.createFileName()
    
        if (not os.path.exists(file)):
            print("No such dir/file as '"+file+"'")
            return
    
        if (not os.path.isfile(file)):
            print("No such file as '"+file+"'")
            return
    
        print("--->parse_file(" + file + ")")
    
        text = ''

        f = open(file, "rb")

        text = f.read(10000000)
        text = u.encode2Ascii(text)
        f.close()

    
        try:
            parser=Entry.Parser
            if (self.get('parser')):
                parser=self.get('parser')

        
            print("soup = BeautifulSoup(text, " + str(parser) +")")
           
            if (parser == None):
                soup = BeautifulSoup(text)
            else:
                if (parser == "html5lib"):
                    soup = BeautifulSoup(text, html5lib)
                else:
                    soup = BeautifulSoup(text, parser)

        except:
            print("ERROR: Failed to parse html file: " + file)
            print(traceback.format_exc())
            return '<br> Failed to parse ' + file + '\n' + text
    
        try:
            print("Original encoding = " + str(soup.originalEncoding))
        except:
            print("Original encoding = <exception>")
    
        body = soup.body
    
        if (body == None):
            return ""
    
        self.dinfo_text = self.dinfo_text + "<b> Searching in file '" + file + "'</b><br>\n"


    
        for key in self.fields:
            if (key[0:5] == "root_"):
                attr_val=self.fields[key]
    
                parts=key.split("_")
                tag=parts[1]
                attr=parts[2]
                
                try:
                    return self.get_subtree_from_html(file, body, tag, attr, attr_val)
                except:
                    if (attr == "class"):
                        attr="id"
    
                    try:
                        return self.get_subtree_from_html(file, body, tag, attr, attr_val)
                    except:
                        pass
    
        root_div_class = None
        if ('root_div_class' in self.fields):
            root_div_class = self.get('root_div_class')
            try:
                return self.get_subtree_from_html(file, body, 'div', 'class', root_div_class)
            except:
                if (not 'root_div_id' in self.fields):
                    print("Trying as 'root_div_id'")
                    self.fields['root_div_id'] = root_div_class
    
        root_div_id = None
        if ('root_div_id' in self.fields):
            root_div_id = self.get('root_div_id')
    
            try:
                return self.get_subtree_from_html(file, body, 'div', 'id', root_div_id)
            except:
                pass

    
        if (not root_div_class == 'content'):
            root_div_class = 'content'
            try:
                return self.get_subtree_from_html(file, body, 'div', 'class', root_div_class)
            except:
                pass
    
        if (not root_div_id == 'content'):
            root_div_id='content'
            try:
                return self.get_subtree_from_html(file, body, 'div', 'id', root_div_id)
            except:
                pass
 
        if (body):
            self.dinfo_text = self.dinfo_text + "Used full body<br>\n"
            return body.contents
    

        print("Returning NO content")
        return ""
