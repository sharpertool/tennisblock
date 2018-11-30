angular.module('tennisblock', [])
//.config()
  .controller('BlockSchedule', function($scope, $http) {
    $scope.dates = []
    $scope.guys = []
    $scope.gals = []
    $scope.subs = []
    $scope.queryDate = null
    $scope.initialized = false
    
    var updateInitialized = function() {
      if ($scope.dates.length > 0
        && $scope.guys.length > 0
        && $scope.gals.length > 0) {
        $scope.initialized = true
      } else {
        $scope.initialized = false
      }
      
      $scope.isLastDate = isLastBlockDate()
      $scope.isFirstDate = isFirstBlockDate()
    }
    
    $http.get('/api/blockdates').success(function(data) {
      $scope.dates = data
      $scope.firstDate = tb.utils.pyDate2js(data[0].date)
      $scope.lastDate = tb.utils.pyDate2js(data[data.length - 1].date)
      $scope.blocksched = {}
      _.each(data, function(d) {
        var bdate = tb.utils.pyDate2js(d.date)
        var ho = d.holdout
        $scope.blocksched[bdate] = ho
      })
      updateInitialized()
    })
    
    var updateAll = function() {
      $scope.initialized = false
      
      $http({
        'url': '/api/blockplayers/date}/',
        'method': 'GET',
        'params': {'date': $scope.queryDate}
      }).success(function(data) {
        $scope.currdate = tb.utils.pyDate2js(data.date).toLocaleDateString()
        $scope.guys = data.guys
        $scope.gals = data.gals
        updateInitialized()
      })
      
      $http({
        'url': '/api/subs/',
        'method': 'GET',
        'params': {'date': $scope.queryDate}
      }).success(function(data) {
        $scope.subs = data
        updateInitialized()
      })
      
      $http({
        'url': '/api/blockschedule/',
        'method': 'GET',
        'params': {'date': $scope.queryDate}
      }).success(function(data) {
        $scope.slots = data
        updateInitialized()
      })
    }
    
    var isLastBlockDate = function() {
      if ($scope.lastDate && $scope.currdate) {
        return $scope.currdate == $scope.lastDate.toLocaleDateString()
      }
      
      return false
    }
    
    var isFirstBlockDate = function() {
      if ($scope.firstDate && $scope.currdate) {
        return $scope.currdate == $scope.firstDate.toLocaleDateString()
      }
      return false
    }
    
    var previousBlockDate = function() {
      var d1 = new Date($scope.currdate)
      if (d1.toDateString() == $scope.firstDate.toDateString()) {
        return d1
      }
      var d2 = new Date(d1.getFullYear(), d1.getMonth(), d1.getDate() - 7)
      while (d2.toDateString() != $scope.lastDate.toDateString() && $scope.blocksched[d2] == 1) {
        d2 = new Date(d2.getFullYear(), d2.getMonth(), d2.getDate() - 7)
      }
      
      return d2
    }
    
    var nextBlockDate = function() {
      var d1 = new Date($scope.currdate)
      if (d1.toDateString() == $scope.lastDate.toDateString()) {
        return d1
      }
      var d2 = new Date(d1.getFullYear(), d1.getMonth(), d1.getDate() + 7)
      while (d2.toDateString() != $scope.lastDate.toDateString() && $scope.blocksched[d2] == 1) {
        d2 = new Date(d2.getFullYear(), d2.getMonth(), d2.getDate() + 7)
      }
      
      return d2
    }
    
    /**
     * schedulePlayer
     *
     * Update the schedule for the current block session
     */
    $scope.schedulePlayer = function() {
    
    }
    
    $scope.isHoldout = function() {
    
    }
    
    $scope.gotodate = function(date) {
      $scope.queryDate = date
      updateAll()
    }
    
    $scope.previous = function() {
      var d1 = previousBlockDate()
      $scope.queryDate = tb.utils.jsDate2py(d1)
      updateAll()
    }
    
    $scope.next = function() {
      $scope.queryDate = tb.utils.jsDate2py(nextBlockDate())
      updateAll()
    }
    
    updateAll()
  })
  .controller('LatestBuzz', function($scope, $http) {
    $http.get('/api/buzz/').success(function(data) {
      $scope.buzzitems = data
    })
  })
  .controller('BlockPlayers', function($scope, $http) {
    $scope.couples = []
    
    $http.get('/api/blockplayers').success(function(data) {
      $scope.couples = data
    })
    
  })
  .controller('Availability', function($scope, $http) {
    $scope.dates = []
    $scope.players = []
    $scope.initialized = false
    
    var updateInitialized = function() {
      if ($scope.dates.length > 0 && $scope.players.length > 0) {
        $scope.initialized = true
      } else {
        $scope.initialized = false
      }
    }
    
    $http.get('/api/blockdates').success(function(data) {
      $scope.dates = data
      updateInitialized()
    })
    $http.get('/api/availability').success(function(data) {
      console.log('calling availability from module')
      $scope.players = data
      updateInitialized()
    })
    
    $scope.isHoldout = function() {
    
    }
    
    $scope.updateAvail = function(p, idx) {
      console.log('Updating for player ' + p.id + " index " + idx + " is avail?" + p.isavail[idx])
      $http.put('/api/availability/', {
        'id': p.id,
        'mtgidx': idx,
        'isavail': p.isavail[idx]
      })
    }
    
    $scope.computeNeeded = function() {
      //$scope.funding.needed = $scope.funding.startingEstimate * 10;
    }
    
    $scope.requestFunding = function() {
      window.alert("Sorry")
    }
    
    $scope.reset = function() {
      //$scope.funding.startingEstimate = 0;
    }
    
    //$scope.$watch('funding.startingEstimate',$scope.computeNeeded);
  })






