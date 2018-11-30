tennisblockapp.factory('BlockDates', function($resource) {
  return $resource('/api/blockdates/', {}, {
    query: {method: 'GET', isArray: true}
  })
}).factory('BlockPlayers', function($resource) {
  return $resource('/api/blockplayers/:date/', {date: '@date'}, {
    get: {method: 'GET', params: {ver: '@ver'}, isArray: false}
  })
}).factory('BlockSubs', function($resource) {
  return $resource('/api/subs/:date/', {date: '@date'}, {
    get: {method: 'GET', params: {ver: '@ver'}, isArray: false}
  })
  
}).factory('PickTeams', function($resource) {
  return $resource('/api/pickteams/:date/', {}, {
    get: {method: 'GET', params: {date: '@date'}, isArray: false},
    save: {method: 'POST', params: {date: '@date'}, isArray: false}
  })
}).factory('PlaySheet', function($resource) {
  return $resource('/api/blocksheet2/:date', {}, {
    get: {method: 'GET', params: {date: '@date'}, isArray: true}
  })
}).factory('TeamSchedule', function($resource) {
  return $resource('/api/matchdata/:date/', {}, {
    get: {method: 'GET', params: {date: '@date', ver: '@ver'}, isArray: false}
  })
}).factory('Availability', function($resource) {
  console.log('calling availability from factory')
  return $resource('/api/availability/', {}, {
    query: {method: 'GET', isArray: true}
  })
}).factory('BlockBuzz', function($resource) {
  return $resource('/api/buzz/', {}, {
    query: {method: 'GET', isArray: true}
  })
}).factory('BlockSchedule', function($resource) {
  return $resource('/api/blockschedule/:date/', {}, {
    get: {method: 'GET', isArray: true},
    remove: {method: 'DELETE', params: {date: '@date'}},
    save: {method: 'POST', params: {date: '@date'}, isArray: false}
  })
}).factory('Members', function($resource) {
  return $resource('/api/members/:id/', {}, {
    get: {method: 'GET', params: {id: '@id'}},
    save: {method: 'POST', isArray: false},
    update: {method: 'POST', params: {id: '@id'}, isArray: false},
    insert: {method: 'PUT', isArray: false},
    remove: {method: 'DELETE'}
  })
}).factory("SendSchedule", function($resource) {
  return $resource('/api/schedule/notify/:date/', {date: '@date'}, {
    get: {method: 'GET', params: {}},
    update: {method: 'POST', params: {}, isArray: false}
  })
})

