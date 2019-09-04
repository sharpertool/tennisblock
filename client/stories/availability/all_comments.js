import range from 'ramda/src/range'

export let comments_gen = []

for (let x in range(0, 20)) {
  comments_gen.push({
    id: x,
    comment: '',
    comment_raw: '',
    comment_rendered: '',
  })
}

export const comments = [
  {
    id: 1,
    author: 'Joe Henderson',
    timestamp: 'Yesterday at 12:30AM',
    comment: 'Lorem ipsum dolor sit amet, vix ad facer nominavi concludaturque, doming ancillae interpretaris eos an. Vix cu sonet percipitur. Duo ridens epicuri ei, epicurie reformidans.',
    comment_raw: 'Lorem ipsum dolor sit amet, vix ad facer nominavi concludaturque, doming ancillae interpretaris eos an. Vix cu sonet percipitur. Duo ridens epicuri ei, epicurie reformidans.',
    avatarurl: 'https://react.semantic-ui.com/images/avatar/small/joe.jpg',
    replies: []
  },
  {
    id: 2,
    author: 'Elliot Fu',
    timestamp: '5 days ago',
    comment: 'Lorem ipsum dolor sit amet, vix ad facer nominavi concludaturque, doming ancillae interpretaris eos an. Vix cu sonet percipitur. Duo ridens epicuri ei, epicurie reformidans.',
    comment_raw: 'Lorem ipsum dolor sit amet, vix ad facer nominavi concludaturque, doming ancillae interpretaris eos an. Vix cu sonet percipitur. Duo ridens epicuri ei, epicurie reformidans.',
    avatarurl: 'https://react.semantic-ui.com/images/avatar/small/elliot.jpg',
    replies: []
  },
  {
    id: 3,
    author: 'Lou Price',
    timestamp: 'January 02, 2018',
    comment: 'Lorem ipsum dolor sit amet, vix ad facer nominavi concludaturque, doming ancillae interpretaris eos an. Vix cu sonet percipitur. Duo ridens epicuri ei, epicurie reformidans.',
    comment_raw: 'Lorem ipsum dolor sit amet, vix ad facer nominavi concludaturque, doming ancillae interpretaris eos an. Vix cu sonet percipitur. Duo ridens epicuri ei, epicurie reformidans.',
    avatarurl: 'https://react.semantic-ui.com/images/avatar/small/matt.jpg',
    replies: []
  },
  {
    id: 4,
    author: 'Lou Price',
    timestamp: 'January 02, 2018',
    comment: 'Lorem ipsum dolor sit amet, vix ad facer nominavi concludaturque, doming ancillae interpretaris eos an. Vix cu sonet percipitur. Duo ridens epicuri ei, epicurie reformidans.',
    comment_raw: 'Lorem ipsum dolor sit amet, vix ad facer nominavi concludaturque, doming ancillae interpretaris eos an. Vix cu sonet percipitur. Duo ridens epicuri ei, epicurie reformidans.',
    avatarurl: 'https://react.semantic-ui.com/images/avatar/small/matt.jpg',
    replies: []
  },
  {
    id: 5,
    author: 'Lou Price',
    timestamp: 'January 02, 2018',
    comment: 'Lorem ipsum dolor sit amet, vix ad facer nominavi concludaturque, doming ancillae interpretaris eos an. Vix cu sonet percipitur. Duo ridens epicuri ei, epicurie reformidans.',
    comment_raw: 'Lorem ipsum dolor sit amet, vix ad facer nominavi concludaturque, doming ancillae interpretaris eos an. Vix cu sonet percipitur. Duo ridens epicuri ei, epicurie reformidans.',
    avatarurl: 'https://react.semantic-ui.com/images/avatar/small/matt.jpg',
    replies: []
  },
  {
    id: 6,
    author: 'Billy Bob',
    timestamp: 'January 02, 2018',
    comment: 'Lorem ipsum dolor sit amet, vix ad facer nominavi concludaturque, doming ancillae interpretaris eos an. Vix cu sonet percipitur. Duo ridens epicuri ei, epicurie reformidans.',
    comment_raw: 'Lorem ipsum dolor sit amet, vix ad facer nominavi concludaturque, doming ancillae interpretaris eos an. Vix cu sonet percipitur. Duo ridens epicuri ei, epicurie reformidans.',
    avatarurl: 'https://react.semantic-ui.com/images/avatar/small/matt.jpg',
    replies: []
  },
]

export const comments_by_id = comments.reduce((acc, c) => {
  acc[c.id] = c
  return acc
}, {})