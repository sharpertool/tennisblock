<?php
/**
 *=-----------------------------------------------------------=
 * htmlgen.inc
 *=-----------------------------------------------------------=
 * Author: Marc Wandschneider:  2005-03-08
 *
 * This is the class that generates most of the common HTML
 * code for our SimpleBlog web application.  The basic
 * sequence of functions you call for a page is:
 *
 * $hg = HtmlGenerator::getInstance();
 * $hg->startPage('page title goes here');
 * $hg->openBody();
 * $hg->emitLeftMenuBar('current page showing');
 * $hg->openContent();
 *  // dump your HTML content here.
 * $hg->closeContent();
 * $hg->closeBody();
 * $hg->closePage();
 */
class HtmlGenerator
{
  /**
   * We only create one instance of these, and this contains
   * that instance.
   */
  private static $s_htmlGenerator;

  /**
   * These are used to help manage state in the generator and
   * ensure correct usage.
   */
  private $m_pageOpened;
  private $m_bodyOpened;
  private $m_contentOpened;

  /**
   *=---------------------------------------------------------=
   * getInstance
   *=---------------------------------------------------------=
   * A static method that returns an instance of the
   * HtmlGenerator object.  We only create one of these, so
   * we return the same instance on repeated calls to this
   * method.
   *
   * Returns:
   *    HtmlGenerator
   */
  public static function getInstance()
  {
    if (HtmlGenerator::$s_htmlGenerator === NULL)
    {
      HtmlGenerator::$s_htmlGenerator = new HtmlGenerator();
    }

    return HtmlGenerator::$s_htmlGenerator;
  }

  /**
   *=---------------------------------------------------------=
   * __construct
   *=---------------------------------------------------------=
   * We don't want anybody to call this except for getInstance
   * above so we made this private.
   */
  private function __construct()
  {
    $this->m_pageOpened = FALSE;
    $this->m_bodyOpened = FALSE;
    $this->m_contentOpened = FALSE;
  }

  /**
   *=---------------------------------------------------------=
   * __destruct
   *=---------------------------------------------------------=
   * cleans up this instance.
   */
  function __destruct()
  {
  }



  /**
   *=---------------------------------------------------------=
   *=---------------------------------------------------------=
   *=---------------------------------------------------------=
   *=---------------------------------------------------------=
   *                      Public Methods
   *=---------------------------------------------------------=
   *=---------------------------------------------------------=
   *=---------------------------------------------------------=
   *=---------------------------------------------------------=
   */

  /**
   *=---------------------------------------------------------=
   * startPage
   *=---------------------------------------------------------=
   * This routine starts a page by emitting the XHTML headers
   * and the <head> portion of the HTML.
   *
   * Parameters:
   *    $in_pageTitle       - the title for this page.
   */
  public function startPage($in_pageTitle)
  {
    if ($this->m_pageOpened)
    {
      throw new IncorrectUsageException('The startPage() method has already been called!');
    }

    $this->m_pageOpened = TRUE;
    echo <<<EOHEAD
<!DOCTYPE html PUBLIC "~//W3C//DTD XHTML 1.0 Transitional//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en-US"
      xml:lang="en-US">
<head>
  <title>$in_pageTitle</title>
  <meta http-equiv="content-type"
        content="text/html; charset=utf-8"/>
  <link rel="stylesheet" href="basestyle.css" type="text/css"/>
</head>

EOHEAD;
  }


  /**
   *=---------------------------------------------------------=
   * closePage
   *=---------------------------------------------------------=
   * We are finished generating the page, so emit the final
   * closing </html> tag.
   */
  public function closePage()
  {
    if ($this->m_bodyOpened)
    {
      throw new IncorrectUsageException('The closeBody() method has not been called to close the body.');
    }
    else if ($this->m_contentOpened)
    {
      throw new IncorrectUsageException('The closeContent() method has not been called to close the page contents');
    }
    else if (!$this->m_pageOpened)
    {
      throw new IncorrectUsageException('The startPage() method was never called to open the page body');
    }

    $this->m_pageOpened = FALSE;
    echo "</html>\n";
  }


  /**
   *=---------------------------------------------------------=
   * openBody
   *=---------------------------------------------------------=
   * Opens the body of the page so that we can start emitting
   * content for it.   This routine is currently not terribly
   * complex!  Our body is basically one giant table, the first
   * column of which is for the left menu bar and the second
   * of which is for the page content.
   */
  public function openBody()
  {
    if (!$this->m_pageOpened)
    {
      throw new IncorrectUsageException('The startPage() method has not yet been called to generate XHTML headers');
    }
    else if ($this->m_bodyOpened)
    {
      throw new IncorrectUsageException('The openBody method has already been called.');
    }

    $this->m_bodyOpened = TRUE;
    echo <<<EOBOPEN
<body>
<table width='100%' border='0' cellspacing='0' cellpadding='3'>
  <table width='100%' border='1' cellspacing='0'
         cellpadding='3' class='titleTable'>
  <tr>
    <td width='100%' class='titleCell'>
      &nbsp;&nbsp;simple blog&nbsp;&nbsp;
      <font class='titleSmall'>
        (not just for professionals)
      </font>
    </td>
  </tr>
  </table>
</table>
<br/>
<table width='100%' border='0' cellspacing='0' cellpadding='3'>
<tr>

EOBOPEN;
  }


  /**
   *=---------------------------------------------------------=
   * closeBody
   *=---------------------------------------------------------=
   * This closes off the page body, including the table that
   * holds the page contents and the left menu bar.
   */
  public function closeBody()
  {
    if (!$this->m_bodyOpened)
    {
      throw new IncorrectUsageException('The openBody() method was never called to open the page body');
    }

    $this->m_bodyOpened = FALSE;
    echo <<<EOBCLOSE
</tr>
</table>
</body>

EOBCLOSE;
  }


  /**
   *=---------------------------------------------------------=
   * emitLeftMenuBar
   *=---------------------------------------------------------=
   * This generates the menu bar that goes along the left edge
   * of our pages.
   *
   * Notes:
   *    We generate different menus depending on whether or not
   *    anybody is logged in or not.  All users see:
   *
   *    - Home (View Users)
   *    - My Entries
   *    - Write New Entry
   *
   *    If you are logged in:
   *    - Logout
   *
   *    If not logged in:
   *    - Login
   *    - Create New Account
   */
  public function emitLeftMenuBar()
  {
    global $g_loggedInUID;

    if (!$this->m_bodyOpened)
    {
      throw new IncorrectUsageException('The openBody() method has not been called to open the page body');
    }

    /**
     * Generate the common items first:
     */
    if ($g_loggedInUID != -1)
    {
      $url = "showentries.php?uid={$g_loggedInUID}";
    }
    else
    {
      $url = "login.php";
    }
    echo <<<EOCOMMON
  <td width='150' valign='top'>
    <table width='100%' border='1' cellspacing='0'
           cellpadding='0'>
    <tr>
      <td width='100%'>
        <table width='100%' border='0' cellspacing='1'
               cellpadding='2' class='menuBarTable'>
        <tr>
          <td width='100%' class='menuBarMenuItem'>
            <a class='menuItem' href='index.php'>
            Home (View Users)
            </a>
          </td>
        </tr>
        <tr>
          <td width='100%' class='menuBarMenuItem'>
            <a class='menuItem'
               href='{$url}'>
              My Journal Entries
            </a>
          </td>
        </tr>
        <tr>
          <td width='100%' class='menuBarMenuItem'>
            <a class='menuItem' href='newentry.php'>
              Write New Entry
            </a>
          </td>
        </tr>
        <tr>
          <td width='100%' class='menuBarMenuItem'>
           <hr size='1'/>
          </td>
        </tr>
EOCOMMON;

    /**
     * Now, emit different goop depending on whether or not
     * we are logged in ...
     */
    if ($g_loggedInUID != -1)
    {
      echo <<<EOLOGGEDIN
        <tr>
          <td width='100%' class='menuBarMenuItem'>
            <a class='menuItem' href='logout.php'>
              Logout
            </a>
          </td>
        </tr>

EOLOGGEDIN;
    }
    else
    {
      echo <<<EONOTLOGGEDIN
        <tr>
          <td width='100%' class='menuBarMenuItem'>
            <a class='menuItem' href='login.php'>
              <b>Login</b>
            </a>
          </td>
        </tr>

        <tr>
          <td width='100%' class='menuBarMenuItem'>
            <a class='menuItem' href='createnewacct.php'>
              Create New Account
            </a>
          </td>
        </tr>

EONOTLOGGEDIN;
    }

    /**
     * Finally, generate the last common bit for the two of
     * these situations.
     */
    echo <<<EOCOMMON
        <tr><td width='100%'>&nbsp;</td></tr>
        </table>
      </td>
    </table>
  </td>

EOCOMMON;
  }


  /**
   *=---------------------------------------------------------=
   * openContent
   *=---------------------------------------------------------=
   * Opens up that portion of the page that holds the
   * individual content.
   */
  public function openContent()
  {
    if (!$this->m_bodyOpened)
    {
      throw new IncorrectUsageException('The openBody() method was never called to open the page body');
    }
    else if ($this->m_contentOpened)
    {
      throw new IncorrectUsageException('The openContent() method has already been called to open the page contents.');
    }

    $this->m_contentOpened = TRUE;
    echo <<<EOOPEN
  <td align='left' valign='top' class='pageContentCell'>
    <table align='center' width='95%' border='0'
           cellspacing='0' cellpadding='0'>
    <tr>
      <td width='100%'>

<!--
     ********************************************************
     BEGIN PAGE CONTENT HERE
     ********************************************************
     It is highly unlikely that the indenting of this
     content will be exactly like that of the rest of the page
     generated by the HtmlGenerator clas
     ********************************************************
  -->

EOOPEN;
  }


  /**
   *=---------------------------------------------------------=
   * closeContent
   *=---------------------------------------------------------=
   * Closes off the portion of the page that holds the
   * individual pages' contents.
   */
  public function closeContent()
  {
    if (!$this->m_contentOpened)
    {
      throw new IncorrectUsageException('The openContent() method has not been called to open the page contents');
    }

    $this->m_contentOpened = FALSE;
    echo <<<EOCONTENTS
<!--
     ********************************************************
     END PAGE CONTENT HERE
     ********************************************************
     It is highly unlikely that the indenting of this
     content will be exactly like that of the rest of the page
     generated by the HtmlGenerator clas
     ********************************************************
  -->
      </td>
    </tr>
    </table>
  </td>

EOCONTENTS;
  }


  /**
   *=---------------------------------------------------------=
   * emitJournalEntry
   *=---------------------------------------------------------=
   * This function takes the various information related to a
   * journal entry and emits it in some pleasant UI form.
   * The default/current action is to put it in a box (table)
   * with a nice little border around it.  We use various
   * pieces of CSS to help with colours, etc...
   *
   * Parameters:
   *    $in_entry               - Entry object to display.
   */
  public function emitJournalEntry
  (
    Entry $in_entry
  )
  {
    /**
     * First, one little thing:  replace newlines in the entry
     * body with <br/> tags so that the formatting appears the
     * same as when the user wrote it.  Note that we do not
     * actually replace these newlines in the data stored in
     * the database because we might have other (non-HTML)
     * uses for these data ...
     */
    $body = ereg_replace('\n', '<br/>', $in_entry->Body);
    echo <<<EOENTRY

<table width='90%' border='2' cellspacing='0' cellpadding='0'>
<tr>
  <td width='100%'>
    <table width='100%' border='0' cellspacing='0'
           cellpadding='4' class='entryTable'>
    <tr>
      <td width='70%' align='left'>
        <a class='entryTitleLink'
           href='showentry.php?eid={$in_entry->EntryID}'>
        {$in_entry->Title}
        </a>
      </td>
      <td align='right' class='entryDate'>
        {$in_entry->Posted}
      </td>
    </tr>
    <tr>
      <td colspan='2'><hr size='1'/></td>
    </tr>
    <tr>
      <td colspan='2' class='entryBody'>
        {$body}
      </td>
    </tr>
    <tr>
      <td colspan='2' width='100%' align='right'>
        <a class='entryWriteCommentLink'
           href='newcomment.php?eid={$in_entry->EntryID}'>
          Add a Comment
        </a>
      </td>
    </tr>
    </table>
  </td>
</tr>
</table>
<br/>

EOENTRY;
  }

  /**
   *=---------------------------------------------------------=
   * emitJournalComment
   *=---------------------------------------------------------=
   * This function takes the various information related to a
   * journal comment and emits it in some pleasant UI form.
   * The default/current action is to put it in a box (table)
   * with a nice little border around it.  We use various
   * pieces of CSS to help with colours, etc...
   *
   * Parameters:
   *    $in_comment         - Comment object with details.
   */
  public function emitJournalComment
  (
    Comment $in_comment
  )
  {
    /**
     * First, one little thing:  replace newlines in the
     * comment body with <br/> tags so that the formatting
     * appears the same as when the user wrote it.  Note that
     * we do not actually replace these newlines in the data
     * stored in the database because we might have other
     * (non-HTML) uses for these data ...
     */
    $body = ereg_replace('\n', '<br/>', $in_comment->Body);
    echo <<<EOCOMMENT

<table width='90%' border='1' cellspacing='0' cellpadding='0'>
<tr>
  <td width='100%'>
    <table width='100%' border='0' cellspacing='0'
           cellpadding='4' class='commentTable'>
    <tr>
      <td class='commentTitle'>
        Title: {$in_comment->Title}
      </td>
    </tr>
    <tr>
      <td class='commentDate'>
        {$in_comment->Posted}
      </td>
    </tr>
    <tr>
      <td align='left' class='commentTitle'>
        By:
        <a class='entryTitleLink'
           href='showentries.php?uid={$in_comment->AuthorID}'>
        {$in_comment->AuthorName}
        </a>
      </td>
    </tr>
    <tr>
      <td colspan='2'><hr size='1'/></td>
    </tr>
    <tr>
      <td colspan='2' class='entryBody'>
        {$body}
      </td>
    </tr>
    </table>
  </td>
</tr>
</table>
<br/>

EOCOMMENT;
  }


}

?>
