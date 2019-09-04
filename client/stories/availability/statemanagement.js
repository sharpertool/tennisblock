import { Store } from '@sambego/storybook-state';
import _ from 'lodash';

function insertItem(array, index, item) {
  return [...array.slice(0, index), item, ...array.slice(index)];
}

function nestComments(commentList) {
  const commentMap = {};

  // move all the comments into a map of id => comment
  commentList.forEach(comment => (commentMap[comment.id] = comment));
  // iterate over the comments again and correctly nest the children
  commentList
    .filter(comment => comment.parentId !== null)
    .forEach(comment => {
      const parent = commentMap[comment.parentId];
      parent.replies.push(comment);
      // dedupe
      parent.replies = _.uniqBy(parent.replies, function(c) {
        return c.id;
      });
    });

  // filter the list to return a list of correctly nested comments
  return commentList.filter(comment => {
    return comment.parentId === null;
  });
}

const commentStore = new Store({
  commentsForRendering: nestComments(commentsInDb),
  commentsInDb: commentsInDb
});

export const getStore = () => {
  return commentStore;
};

export const addComment = comment => {
  const current_comments_state = commentStore.get('commentsInDb');
  const sample_comment_object = {
    id: Math.round(Math.random() * 100 + 1).toString(),
    author: 'Joe Henderson',
    timestamp: new Date().toDateString(),
    commentText: comment,
    parentId: null,
    depth: 0,
    replies: [],
    avatarurl: 'https://react.semantic-ui.com/images/avatar/small/joe.jpg'
  };
  const updated_comment_state = insertItem(
    current_comments_state,
    0,
    sample_comment_object
  );
  commentStore.set({
    commentsForRendering: nestComments(updated_comment_state),
    commentsInDb: updated_comment_state
  });
};

