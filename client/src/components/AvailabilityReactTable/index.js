import React from 'react'

import ReactTable from 'react-table'
import withFixedColumns from 'react-table-hoc-fixed-columns'
import 'react-table/react-table.css'
import 'react-table-hoc-fixed-columns/lib/styles.css'

const ReactTableFixed = withFixedColumns(ReactTable)

const Availability = ({
                        blockdates,
                        availability,
                        availabilityChanged,
                      }) => {
  
  const getColumnWidth = (data, accessor, headerText) => {
    if (typeof accessor === 'string' || accessor instanceof String) {
      accessor = d => d[accessor] // eslint-disable-line no-param-reassign
    }
    const maxWidth = 600
    const magicSpacing = 10
    const cellLength = Math.max(
      ...data.map(row => (`${accessor(row)}` || '').length),
      headerText.length,
    )
    const wval = Math.min(maxWidth, cellLength * magicSpacing)
    console.log(`Width val: ${wval}`)
    return wval
  }
  
  const onAvailChanged = (dprops, idx) => {
    const {original: player} = dprops
    console.dir(player)
    availabilityChanged({
      id: player.id,
      mtgidx: idx,
      isavail: !player.isavail[idx]
    })
  }
  
  const data = availability
  const columns = [
    {
      Header: 'Name',
      accessor: 'name',
      filterable: true,
      filterMethod: (filter, row) => {
        return row[filter.id].toLowerCase().includes(filter.value.toLowerCase())
      },
      fixed: 'left',
      width: getColumnWidth(data, d => d.name, 'Name')
    },
  ]
  blockdates.map((bd, idx) => {
    const d = new Date(bd.date.split('-'))
    const dstring = d.toLocaleDateString('en',
      {month: 'short', day: 'numeric'}
    )
    columns.push({
      id: `date-${bd.date}`,
      index: idx,
      Header: dstring,
      headerClassName: bd.holdout ? 'holdout' : 'play',
      accessor: d => d.isavail[idx],
      Cell: row => {
        return (
          <input type="checkbox"
                 checked={row.value}
                 onChange={() => onAvailChanged(row, idx)}
          />
        )
      }
      
    })
  })
  columns.push({
    Header: '# Played',
    accessor: 'nplayed',
  })
  columns.push({
    Header: '# Scheduled',
    accessor: 'nscheduled',
  })
  
  return (
    <ReactTableFixed
      data={data}
      columns={columns}
      className="-striped"
      getTdProps={(state, row, column, instance) => {
        let classes = []
        if (row && column) {
          const {original: player} = row
          const {index: idx} = column
          const is_scheduled = player.scheduled[idx]
          const did_play = player.played[idx]
          if (is_scheduled) {
            classes.push('scheduled')
          }
          if (did_play) {
            classes.push('played')
          }
          return {
            onClick: (e) => {
              onAvailChanged(row, idx)
            },
            className: classes.join(' '),
          }
        }
        return {
          className: classes.join(' '),
        }
      }}
    />
  )
}

export default Availability