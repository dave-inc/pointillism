import React from 'react';
import Typography from '@material-ui/core/Typography';
// import PayPalExpressButton from './payments/PayPalExpressButton'

// <p>Source: <a href={resource}>{resource}</a></p>
function DOTDetail() {
  const hostname = `${window.location.protocol}//${window.location.hostname}:${window.location.port}`;
  const path = window.location.href.split("#")[1];
  const render = `${hostname}${path}`
    
  return (
    <Typography align="center" paragraph={true}>
      <h2>{path}</h2>
      <div>
      <img src={render} alt={path} />
      </div>
      <p>formats:&nbsp;
        <a href={path + ".svg"}>svg</a>&nbsp;
        <a href={path + ".png"}>png</a>&nbsp;
        <a href={path + ".jpg"}>jpeg</a>
      </p>
    
      <div className="example">
        <p class="center">
          <code>&lt;img src="{render}.svg"/&gt;</code>
          <br/>
        </p>
      </div>

    </Typography>
  )
  // <PayPalExpressButton/> 
}

export default DOTDetail;
