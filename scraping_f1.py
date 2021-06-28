  def diff_page(self, classId, NEW_DIR, OLD_DIR, email_attrs):
        itemno=0
    
        new_lines = self.parse_page(NEW_DIR)
        try:
            new_lines = str(new_lines) # to UTF-8
        except:
            print("ERROR: Failed to str(NEW page)")
            raise
            #return ""
    
        try:
            new_lines = ''.join(new_lines)
            new_lines = new_lines.decode("utf8")
        except:
            print("ERROR: Failed to decode NEW page to 'utf8'")
            #raise
            #return ""
    
        if ((new_lines != "") and email_attrs['SEND_MAIL_INDIVIDUAL']):
            #body = ''.join(lines.readlines())
            #body = new_lines
            body = u.encode2Ascii(new_lines)
    
            if (('action' in self.fields) and (self.get('action')  == "email_selection")):
                print("email_selection")
    
                select_entries=email_attrs['select_entries']
                category=email_attrs['category']
                period=email_attrs['period']
                name=email_attrs['name']
                send_to= [ email_attrs['SEND_TO'] ]
                u.sendmail( self, send_to, body, select_entries, category, period, "SELECT: " + name, Entry.globalRunID)
                return ""
    
        try:
            old_lines = self.parse_page(OLD_DIR)
        except:
            print("ERROR: Failed to parse_page(OLD page)")
            raise
    
        try:
            old_lines = str(old_lines) # to UTF-8
        except:
            print("ERROR: Failed to str(OLD page)")
            old_lines = ""
            #raise
            #return ""
    
        try:
            old_lines = ''.join(old_lines)
            old_lines = old_lines.decode("utf8")
        except:
            print("ERROR: Failed to decode OLD page to 'utf8'")
    
    
        
        file = NEW_DIR + "/" + self.createFileName() + ".new.prediff"
        u.writeFile(file, u.encode2Ascii(new_lines))
        file = NEW_DIR + "/" + self.createFileName() + ".old.prediff"
        u.writeFile(file, u.encode2Ascii(old_lines))
    
        print("   diff("+str(len(old_lines))+" old bytes vs. "+str(len(new_lines))+" new bytes)")
        diff_text = difflib.unified_diff(old_lines.split("\n"), new_lines.split("\n"))
        
    
        if self.debug:
            try:
     
                print("Writing diff file: " + file)
                debug_diff_text = diff_text[:] 
                debug_diff_text = ' '.join(list(debug_diff_text))
                print("debug_diff_text len="+str(len(debug_diff_text)))
                debug_diff_text = u.encode2Ascii(debug_diff_text)
                print("debug_diff_text len="+str(len(debug_diff_text)))
                u.writeFile(file, debug_diff_text)
            except:
                print("ERROR: failed to write diff file: " + traceback.format_exc())
    
        show_new_only=True
        show_new_only=False
    
        div_page_diffs = "<hr>\n<div class id='"+classId+"'>\n"

    
        itemno = itemno +1
        item=str(itemno)
        div_page_diffs = div_page_diffs + "<a name='item_"+item+"'> </a>\n"
        div_page_diffs = div_page_diffs + "<h1> "+classId+" </h1>\n"
    
        page_diffs = ""
    
        for d in diff_text:
            d = d.encode("utf8", "ignore")
            d = d.decode()
    
            if (d.find("+++") == 0): 
                continue
    
            if (d.find("@@") == 0):
                continue
    
            if (d.find("-") == 0): 
                continue
    
            d = self.substitute_local_links(d)
    
            if (d.find("+") == 0): 
                d = d.replace("+","",1).replace("u[\"","",1)
                if (show_new_only):
                    page_diffs = page_diffs + d + "\n";

                    continue

    
            if ( not show_new_only):

                page_diffs = page_diffs + d + "\n";

    
        print("   ==> "+str(len(page_diffs))+" NEW bytes different")
    
        if (page_diffs == ""):
            return ""
    
        if self.debug:
            try:
                file = NEW_DIR + "/" + self.createFileName() + ".diff.NEW"
                print("Writing diff file: " + file)
                debug_page_diffs = page_diffs[:] # Deepcopy !!
                debug_page_diffs = ' '.join(list(debug_page_diffs))
                print("debug_page_diffs len="+str(len(debug_page_diffs)))
                debug_page_diffs = u.encode2Ascii(debug_page_diffs)
                print("debug_page_diffs len="+str(len(debug_page_diffs)))
                u.writeFile(file, debug_page_diffs)
            except:
                print("ERROR: failed to write diff file: " + traceback.format_exc())
        page_diffs = div_page_diffs + page_diffs + "</div><<br/> <!-- "+classId+"-->\n\n"
    
        if ((page_diffs != "") and email_attrs['SEND_MAIL_INDIVIDUAL']):
  
            body = page_diffs.encode('utf-8')
    
            select_entries=email_attrs['select_entries']
            category=email_attrs['category']
            period=email_attrs['period']
            name=email_attrs['name']
            send_to= [ email_attrs['SEND_TO'] ]
            u.sendmail( self, send_to, body, select_entries, category, period, name, Entry.globalRunID)
    
        return page_diffs
    


    def check_file_not_gzipped(self, file):
    
        byte1 = 0
        byte2 = 0
    
        with open(file, 'rb') as fp:
            byte1 = ord(fp.read(1))
            byte2 = ord(fp.read(1))
    
        if (byte1 == 0x1f) and (byte2 == 0x8b):
            print("File '" + file + "' is gzip-compressed, uncompressing ...")
            ifp = gzip.open(file, 'rb')
            content = ifp.read()
            ifp.close()
    
            u.writeFile(file, content)
     

    
    def substitute_local_links(self, d):
    
       file_slash=d.find('href="/')
    
       if (file_slash < 0):
           file_slash=d.find("href='/")
    
           if (file_slash < 0):
               return d
    
       slash=self.url.find("/")
    
       protocol = self.url[:slash-1]
       addr = self.url[slash+2:]
       slash3 = addr.find("/")
    

    
       orig = d
    
       rootUrl = protocol + "://" + addr[:slash3] + "/"

    
       d = d.replace("href='/", "href='"+rootUrl)
       d = d.replace('href="/', 'href="'+rootUrl)
      

    
       return d
