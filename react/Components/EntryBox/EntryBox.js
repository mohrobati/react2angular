//import React from 'react'
//import './EntryBox.css'

function EntryBox(props) {
    return (
        <div className="EntryBox" style={{background: props.color}}>
            <h2>{props.title}</h2>
            <br />
            <img src={props.img} />
        </div>
    )
}

//export default EntryBox;