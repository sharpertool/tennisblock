<?php
	/**
	 * Created by IntelliJ IDEA.
	 * User: kutenai
	 * Date: 9/15/13
	 * Time: 2:51 PM
	 * To change this template use File | Settings | File Templates.
	 */


	include "Schedule.php";

	$sch = ScheduleManager::getInstance();

	$seasons = $sch->getSeasons();

	$fmdate = $sch->getFirstMatchDate();
	$lbd = $sch->lastBlockDate();

	$match_id = $sch->getMatchid(strtotime("2013-09-20"));

	$ho = $sch->isHoldout(strtotime("2013-09-20"));

	$mbyid = $sch->getMatchByID($match_id);

	$group = $sch->getNExtGroup(strtotime("2013-09-20"));

	echo "Done";
