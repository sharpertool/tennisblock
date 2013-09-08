<?php
/**
 *=-----------------------------------------------------------=
 * ScheduleManager.inc
 *=-----------------------------------------------------------=
 * Author: Ed Henderson
 *
 * The ScheduleManger class is responsible for updating, and
 * manipulationg scedules
 */
require_once('../inc/dbmanager.php');
require_once('../inc/Player.php');

class Team
{
    public $team;
    public $set;
    public $court;
    public $combokey;

    public function __construct($set,$court)
    {
        $this->set = $set;
        $this->court = $court;
    }
    
    public function setPlayers($t1,$t2)
    {
        $team = array();
        $this->team['tapa']  = $t1[0];
        $this->team['tapb']  = $t1[1];
        $this->team['tbpa']  = $t2[0];
        $this->team['tbpb']  = $t2[1];
    }
    
    public function insertRecord($matchid) {
        /**
        * Get a database connection with which to work.
        */
        $conn = DBManager::getConnection();
        
        /**
        * Build a query to ask if there is any overlap.
        */
        $query = "insert into slots (matchid,setnum,court,pid,position,combokey) " .
        " values  ";
        $values = array();
        $combokey = "''";
        
        foreach (array('tapa','tapb','tbpa','tbpb') as $pos) {
            $p = $this->team[$pos];
            $id = $p->pid;
            $position = "'$pos'";
            $values[] = "( " . implode(",",array($matchid,$this->set,$this->court,$id,$position,$combokey)) . ")";
        }

        $query .= implode(",",$values);
        
        $results = @$conn->query($query);
        if ($results == FALSE or $results == NULL)
            throw new DatabaseErrorException($conn->error);
    }
    
    public static function clearTeams($matchid)
    {
        /**
        * Get a database connection with which to work.
        */
        $conn = DBManager::getConnection();
        
        // Fill the tmp_players table with players for this block
        $query = "delete from slots where matchid = $matchid";
        $results = @$conn->query($query);
        if ($results == FALSE or $results == NULL)
            throw new DatabaseErrorException($conn->error);
        
    }
    
    public static function resetTmpPlayers($matchid)
    {
        /**
        * Get a database connection with which to work.
        */
        $conn = DBManager::getConnection();
        
        // Fill the tmp_players table with players for this block
        $query = "drop view if exists tmp_players_view;";
        $results = @$conn->query($query);
        if ($results == FALSE or $results == NULL)
            throw new DatabaseErrorException($conn->error);

        // Fill the tmp_players table with players for this block
        $query = "drop table if exists tmp_players;";
        $results = @$conn->query($query);
        if ($results == FALSE or $results == NULL)
            throw new DatabaseErrorException($conn->error);

        $query = "create table tmp_players (pid int(8));";
        $results = @$conn->query($query);
        if ($results == FALSE or $results == NULL)
            throw new DatabaseErrorException($conn->error);

        // Fill the tmp_players table with players for this block
        $query = "insert into tmp_players (select pid from schedule where matchid = $matchid)";
        $results = @$conn->query($query);
        if ($results == FALSE or $results == NULL)
            throw new DatabaseErrorException($conn->error);
            
        $query = <<<EOQUERY
        create view tmp_players_view as
        select 
            p.pid pid,
            firstname,
            lastname,
            gender,
            NTRP,
            microNTRP
        from players p,tmp_players tp
        where
            p.pid = tp.pid
            ;
EOQUERY;
        
        $results = @$conn->query($query);
        if ($results == FALSE or $results == NULL)
            throw new DatabaseErrorException($conn->error);
            
    }
    
    public static function resetTmpCouples($matchid)
    {
        /**
        * Get a database connection with which to work.
        */
        $conn = DBManager::getConnection();

        // Fill the tmp_players table with players for this block
        $query = "drop table if exists tmp_couples;";
        $results = @$conn->query($query);
        if ($results == FALSE or $results == NULL)
            throw new DatabaseErrorException($conn->error);

        $query = <<<EOQUERY
create table tmp_couples (
        cid         integer(16) NOT NULL auto_increment,
        m_pid       integer(16),
        m_name      varchar(60),
        m_ntrp      float,
        m_untrp     float,
        f_pid       integer(8),
        f_name      varchar(60),
        f_ntrp      float,
        f_untrp     float,
        c_ntrp      float,
        c_untrp     float,
        primary key (`cid`)
    );
    
EOQUERY;

        $results = @$conn->query($query);
        if ($results == FALSE or $results == NULL)
            throw new DatabaseErrorException($conn->error);

        $query = <<<EOQUERY
insert into tmp_couples (
        m_pid,
        m_name,
        m_ntrp,
        m_untrp,
        f_pid,
        f_name,
        f_ntrp,
        f_untrp,
        c_ntrp,
        c_untrp
    )
select
    m.pid m_id,
    concat(m.firstname," ",m.lastname) m_name,
    m.NTRP m_ntrp,
    m.microNTRP m_untrp,
    f.pid f_id,
    concat(f.firstname," ",f.lastname) f_name,
    f.NTRP f_ntrp,
    f.microNTRP f_untrp,
    m.NTRP + f.NTRP c_ntrp,
    m.microNTRP + f.microNTRP c_untrp
    
from players m,players f
where 
        m.gender = 'f' 
    and f.gender = 'm'
    and (m.pid in (select pid from schedule where matchid = $matchid))
    and (f.pid in (select pid from schedule where matchid = $matchid))
;
EOQUERY;

        $results = @$conn->query($query);
        if ($results == FALSE or $results == NULL)
            throw new DatabaseErrorException($conn->error);
            
    }
        
    public static function pairExists($matchid,$mid,$fid)
    {
        /**
        * Get a database connection with which to work.
        */
        $conn = DBManager::getConnection();

        $query = <<<EOQUERY
        select count(*) cnt
        from slots s1,slots s2
        where
            s1.matchid = $matchid
            and s2.matchid = $matchid
            and (
                (s1.position = 'tapa' and s2.position = 'tapb')
                    or
                (s1.position = 'tbpa' and s2.position = 'tbpb')
                )
            and s1.pid = $mid and s2.pid = $fid
        ;
        
EOQUERY;

        $results = @$conn->query($query);
        if ($results == FALSE or $results == NULL)
            throw new DatabaseErrorException($conn->error);

        $count = 0;
        while (($row = $results->fetch_assoc()) != NULL) {
            $count = $row['cnt'];
        }
        
        if ($count > 0) {
            return True;
        } else {
            return False;
        }
    }
        
    public static function getTeamPlayers()
    {
        /**
        * Get a database connection with which to work.
        */
        $conn = DBManager::getConnection();

        $query = "select * from tmp_couples";

        $results = @$conn->query($query);
        if ($results == FALSE or $results == NULL)
            throw new DatabaseErrorException($conn->error);
        
        while (($row = $results->fetch_assoc()) != NULL) {
            $team->team[$row['position']] = Player::getPlayer($row['pid']);
        }
        
        
        $nrows = $results->num_rows;
        if ($results->num_rows >= 1)
        {
            $dbrow = @$results->fetch_assoc();
            $team = new Team($set,$court,$dbrow);
        }
        $results->close();
        return $team;
    }
    
    public static function getPlayers()
    {
        /**
        * Get a database connection with which to work.
        */
        $conn = DBManager::getConnection();

        $query = "select * from tmp_players_view";

        $results = @$conn->query($query);
        if ($results == FALSE or $results == NULL)
            throw new DatabaseErrorException($conn->error);
        
        $men = array();
        $women = array();
        while (($row = $results->fetch_assoc()) != NULL) {
            $p = new Player($row);
            if ($p->gender == 'f') {
                $women[] = $p;
            } else {
                $men[] = $p;
            }
        }
        
        return array($men,$women);
    }
    
    public static function getTwoTeams($matchid,$set)
    {
        /**
        * Get a database connection with which to work.
        */
        $conn = DBManager::getConnection();
        
        // Get a list of all pids that are currently scheduled for this match and set.
        // The court does not matter..

        $query = "select pid from slots where matchid = $matchd and setnum = $set";

        $results = @$conn->query($query);
        if ($results == FALSE or $results == NULL)
            throw new DatabaseErrorException($conn->error);
        
        $pids = array();
        while (($row = $results->fetch_assoc()) != NULL) {
            $pids[] = $row['pid'];
        }
        
        $pids = implode(",",$pids);

        $query = <<<EOQUERY
        select
            a.cid
            b.cid
        from
            tmp_couples a,tmp_couples b
        where
                a.pid not in ($pids)
            and b.pid not in ($pids)
            and a.m_pid != b.m_pid
            and a.f_pid != b.f_pid
        ;
EOQUERY;

        $results = @$conn->query($query);
        if ($results == FALSE or $results == NULL)
            throw new DatabaseErrorException($conn->error);
        
        $pids = array();
        while (($row = $results->fetch_assoc()) != NULL) {
            $pid[] = $row['pid'];
        }

        
        $nrows = $results->num_rows;
        if ($results->num_rows >= 1)
        {
            $dbrow = @$results->fetch_assoc();
            $team = new Team($set,$court,$dbrow);
        }
        $results->close();
        return $team;
    }
    
    public static function getTmpCouples()
    {
        /**
        * Get a database connection with which to work.
        */
        $conn = DBManager::getConnection();
        
        /**
        * Build a query to ask if there is any overlap.
        */
        $cols = "cid,m_pid,m_ntrp,m_untrp,f_pid,f_ntrp,f_untrp,c_ntrp,c_untrp";
        $query = "select $cols from tmp_couples";

        $results = @$conn->query($query);
        if ($results == FALSE or $results == NULL)
            throw new DatabaseErrorException($conn->error);

        $team = new Team($set,$court);
        $players = array();
        while (($row = $results->fetch_assoc()) != NULL) {
            $team->team[$row['position']] = Player::getPlayer($row['pid']);
        }
        $results->close();
        return $team;
    }
    public static function getTeam($matchid,$set,$court)
    {
        /**
        * Get a database connection with which to work.
        */
        $conn = DBManager::getConnection();
        
        /**
        * Build a query to ask if there is any overlap.
        */
        $query = "select * from slots where matchid = $matchid and setnum = $set and court = $court";

        $results = @$conn->query($query);
        if ($results == FALSE or $results == NULL)
            throw new DatabaseErrorException($conn->error);

        $team = new Team($set,$court);
        $players = array();
        while (($row = $results->fetch_assoc()) != NULL) {
            $team->team[$row['position']] = Player::getPlayer($row['pid']);
        }
        $results->close();
        return $team;
    }
}

?>