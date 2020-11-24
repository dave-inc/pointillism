import React from 'react';
import Typography from '@material-ui/core/Typography';
// import PayPalExpressButton from './payments/PayPalExpressButton'
function pathToResource(path) {
  const split = path.split("/");
  if (split.length < 3) {
    throw Error("Invalid path for Resource");
  }
  const owner = split[1];
  const project = split[2];
  return {
    owner: owner,
    project: project,
    repo: `${owner}/${project}`,
    filename: split[split.length-1]
  }
}

// <p>Source: <a href={resource}>{resource}</a></p>
function DOTDetail() {
  const hostname = `${window.location.protocol}//${window.location.hostname}:${window.location.port}`;
  const path = window.location.href.split("#")[1];
  const resource = pathToResource(path);
  const render = `${hostname}${path}`;
    
  return (
    <Typography align="center" paragraph={true}>
      <h2>{resource.filename}</h2>
      <p>{resource.repo}</p>
      <div>
      <img src={path + ".svg"} alt={path} />
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
