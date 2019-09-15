import chunk from 'lodash/chunk'
import {connect} from 'react-redux'
import React, {useEffect, useState} from 'react'
import HeaderDate from '~/components/ui/Header/Date'
import {Row, Col, Button, Input} from 'reactstrap'
import {withRouter} from 'react-router-dom'
import ActionButtons from './ActionButtons'
import styled from 'styled-components'
import {BLOCK_TYPE, DraftailEditor, INLINE_STYLE, ENTITY_TYPE} from 'draftail'
import {createEditorStateFromRaw, serialiseEditorStateToRaw} from 'draftail'
import {EditorState, convertFromRaw, convertToRaw} from 'draft-js'
import { convertFromHTML, convertToHTML } from 'draft-convert'

import Couples from './Couples'

const ErrorDiv = styled.div`
  color: red;
`

import {actions, selectors} from '~/redux-page'

import styles from './styles.local.scss'

const exporterConfig = {
  blockToHTML: (block) => {
    if (block.type === BLOCK_TYPE.BLOCKQUOTE) {
      return <blockquote />
    }

    // Discard atomic blocks, as they get converted based on their entity.
    if (block.type === BLOCK_TYPE.ATOMIC) {
      return {
        start: '',
        end: '',
      }
    }

    return null
  },

  entityToHTML: (entity, originalText) => {
    if (entity.type === ENTITY_TYPE.LINK) {
      return <a href={entity.data.url}>{originalText}</a>
    }

    if (entity.type === ENTITY_TYPE.IMAGE) {
      return <img src={entity.data.src} alt={entity.data.alt} />
    }

    if (entity.type === ENTITY_TYPE.HORIZONTAL_RULE) {
      return <hr />
    }

    return originalText
  },
}
const toHTML = (raw) =>
  raw ? convertToHTML(exporterConfig)(convertFromRaw(raw)) : ''


const MeetingNotify = props => {
  
  const initialState = EditorState.createEmpty()

  const [editorState, setEditorState] = useState(initialState)

  const {match, message,
    updateMessage, getBlockPlayers,
    sendNotification,
    errors
  } = props
  
  useEffect(() => {
    // Get initial data
    console.log(match)
    getBlockPlayers({date: match.params.id})
  }, [])

  const onSendNotification = () => {
    const raw = serialiseEditorStateToRaw(editorState)
    const html = toHTML(raw)
    console.log(`Html Content ${html}`)
    sendNotification({message: html})
  }
  
  const onChange = (es) => {
    setEditorState(es)

  }

  const onClickSave = (e) => {
    e.preventDefault()
    console.log('user clicked save')
    //const raw = serialiseEditorStateToRaw(editorState)
    //onSave(raw)
  }

  const onClickCancel = (e) => {
    e.preventDefault()
    //onCancel()
    //setEditorState(restoreState)
  }

  const bottomToolbar = () => (
    <>
      <div >
        <button onClick={onClickSave}
                className="btn btn-primary">
          Save
        </button>
        <button onClick={onClickCancel}
                className="btn btn-secondary">
          Cancel
        </button>
      </div>
    </>
  )

  const editor =
    <DraftailEditor
      className={['col-12',styles.editor].join(' ')}
      showUndoControl={true}
      showRedoControl={true}
      editorState={editorState}
      onChange={(es) => onChange(es)}
      blockTypes={[
        {type: BLOCK_TYPE.HEADER_ONE},
        {type: BLOCK_TYPE.HEADER_TWO},
        {type: BLOCK_TYPE.HEADER_THREE},
        {type: BLOCK_TYPE.UNORDERED_LIST_ITEM},
      ]}
      inlineStyles={[
        {type: INLINE_STYLE.BOLD},
        {type: INLINE_STYLE.ITALIC},
      ]}
      entityTypes={[]}
      //bottomToolbar={bottomToolbar}
    />

  return (
    <div className="matches">
      <HeaderDate
        title="Fun Stuff"
        classNames="mb-4"
        link={`/schedule/${match.params.id}`} date={match.params.id}/>
        <ActionButtons sendNotification={onSendNotification}/>
      {errors.length > 0 ?
        <ErrorDiv>
          <h3>Errors:</h3>
          <ul>
            {errors.map((e,i) => {
              return (
                <li key={i}>{e}</li>
              )
            })}
          </ul>
        </ErrorDiv>
        : null
      }
      <Row className="mb-12">
        <Col className="d-flex justify-content-between">
        </Col>
      </Row>
      <Row>
        <Col md={12}>
          <Couples couples={props.couples}/>
        </Col>
      </Row>
      <Row className={styles.editor_row}>
        <Col>
          {editor}
        </Col>
      </Row>
    </div>
  )
}

const mapStateToProps = (state) => {
  return {
    couples: selectors.getCouples(state),
    message: selectors.notify_message(state),
    errors: selectors.notify_errors(state),
  }
}

const mapDispatchToProps = {
  updateMessage: actions.scheduleNotifyMsgUpdate,
  getBlockPlayers: actions.getBlockPlayers,
  sendNotification: actions.scheduleNotify,
}

export default withRouter(connect(
  mapStateToProps,
  mapDispatchToProps
)(MeetingNotify))
