<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
 <head>
  <title>File Manager</title>
  <script type="text/javascript" src="js/filemanager.js"></script>
  <link rel="stylesheet" href="css/styles.css"/>
 </head>
 <body>
  <div class="datagrid" id="file_datagrid"></div>
  <div id="toolbar">
   <img src="img/open.gif" id="btn_open" style="margin-right: 20px;"
    alt="Download/Open" title="Download/Open"/>
   <img src="img/new.gif" id="btn_new_folder" alt="New" title="New"/>
   <img src="img/upload.gif" id="btn_upload_file" alt="Upload" title="Upload"/>
   <img src="img/rename.gif" id="btn_rename_file" alt="Rename" title="Rename"/>
   <img src="img/delete.gif" id="btn_delete_file" style="margin-right: 20px;"
    alt="Delete" title="Delete"/>
   <form action="process.php?new" id="form_new" method="post" 
    style="display: none;">
    <div>
     <input type="text" name="name" id="form_new_name" />
     <input type="submit" value="Ok" id="form_new_submit" />
     <input type="reset" value="Cancel" id="form_new_reset" />
    </div>
   </form>
   <form action="process.php?rename" id="form_rename" method="post" 
    style="display: none;">
    <div>
     <input type="text" name="name" id="form_rename_name" />
     <input type="submit" value="Ok" id="form_rename_submit" />
     <input type="reset" value="Cancel" id="form_rename_reset" />
    </div>
   </form>
   <form action="upload.php" id="form_upload" method="post" 
    enctype="multipart/form-data" style="display: none;">
    <div>
     <input type="file" name="file" id="form_upload_name" />
     <input type="hidden" name="directory" id="form_upload_directory" value=""/>
     <input type="submit" value="Ok" id="form_upload_submit" />
     <input type="reset" value="Cancel" id="form_upload_reset" />
    </div>
   </form>
   <iframe id="my_iframe" name="my_iframe" style="display:none;"></iframe>
  </div>
 </body>
</html>
