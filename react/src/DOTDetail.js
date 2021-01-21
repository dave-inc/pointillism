import React, { useEffect } from 'react';
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
  // const imgTag =
  
  useEffect(() => {
    const showcase = document.getElementById("showcase");
    fetch(path).then(response => {
      response.text().then(function (text) {
        showcase.innerHTML = text;
      })
    })
  });

  return (
    <Typography align="center" paragraph={true}>
      <h2>{resource.filename}</h2>
      <p>{resource.repo}</p>
      <div id="showcase">
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
      <meta property="og:image" content={`${hostname}${path}.png`} />

    </Typography>
  )
  // <meta property="og:url"          content="http://www.nytimes.com/2015/02/19/arts/international/when-great-minds-dont-think-alike.html" />
  // <meta property="og:title"        content="When Great Minds Don’t Think Alike" />
  // <meta property="og:description"  content="How much does culture influence creative thinking?" />
  // <PayPalExpressButton/> 
}

export default DOTDetail;
