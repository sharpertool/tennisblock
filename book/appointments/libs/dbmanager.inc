<?php
/**
 *=-----------------------------------------------------------=
 * dbmanager.inc
 *=-----------------------------------------------------------=
 * Author: Marc Wandschneider, 2005-03-05
 *
 * This class manages database connections for us.  For the
 * mysqli case, we just create one connection per new instance
 * of the PHP session.
 */
require_once('../libs/dbconninfo.inc');

/**
 *=-----------------------------------------------------------=
 * DBManager
 *=-----------------------------------------------------------=
 */
class DBManager
{
  /**
   * This is the connection we're using for this instance.  It
   * will automagically be closed when our instance closes.
   */
  private static $s_conn;

  /**
   *=---------------------------------------------------------=
   * getConnection
   *=---------------------------------------------------------=
   * Static method to get a connection to the database server
   * with which we are interacting.
   *
   * Returns:
   *    mysqli object representing the connection.  Throws on
   *    failure.
   */
  public static function getConnection()
  {
    if (DBManager::$s_conn === NULL)
    {
      /**
       * Create a new mysqli object, throw on failure.
       */
      $conn = @new mysqli(DB_HOST, DB_USER, DB_PASS, DB_DBASE);
      if (mysqli_connect_errno() !== 0)
      {
        $msg = mysqli_connect_error();
        throw new DatabaseErrorException($msg);
      }

      /**
       * Make sure the connection is set up for utf8
       * communications.
       */
      @$conn->query('SET NAMES \'utf8\'');
      DBManager::$s_conn = $conn;
    }

    return DBManager::$s_conn;
  }


  /**
   *=---------------------------------------------------------=
   * mega_escape_string
   *=---------------------------------------------------------=
   * This is a much improved version of a string manipulator
   * that makes strings safe for:
   *
   * - insertion into our database.
   * - subsequent display in our pages.
   *
   * Specifically, this function:
   *    - prefixes all ', %, and ; characters with
   *        backslashes
   *    - optionally replaces all < and > characters with
   *        the appropriate entity (&lt; and &gt;).
   *
   * Parameters:
   *    $in_string          - string to fix up.
   *    $in_markup          - [optional] replace HTML markup
   *                            < and > ???
   *
   * Returns:
   *    string -- safe!!!!!
   *
   * Notes:
   *    No, ereg_replace is NOT the fastest function ever.
   *    However, it is very UTF-8 safe, which is critcal for
   *    us.  We did some timings, and this took an average of
   *    5x10e-5 seconds per string
   */
  public function mega_escape_string
  (
    $in_string,
    $in_markup = FALSE
  )
  {
    if ($in_string === NULL)
      return '';

    $str = ereg_replace('([\'%;])', '\\\1', $in_string);
    if ($in_markup == TRUE)
    {
      $str = htmlspecialchars($str, ENT_NOQUOTES,
          "UTF-8");
    }

    return $str;
  }


}

?>
