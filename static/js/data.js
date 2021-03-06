/*
  Sample Usage:
  
  var myData = {
    "name": "Root",
    "children": [
      {
        "name": "Branch 1",
        "children": [
          {"name": "Leaf 3"},
          {"name": "Leaf 4"}
        ]
      },
      {"name": "Branch 2"}
    ]
  };
  
  var chart = MindMap()
    .width(900)
    .height(500)
    ;
  
  d3.select('#chart svg')
    .datum(myData)
    .call(chart)
    ;
*/

var MindMap = function(){
  "use strict";
  var 
      margin = {top: 20, left: 120, bottom: 20, right: 120},
      width = 960,
      height = 500,
      duration = 500,
      identity = '_id',
      handleClick = function(){},
      text = function(d){ return d.name; },
      idx = 0,
      enterNode = function(node){
        node.append("svg:circle")
            .attr("r", 1e-6);
        
        node.append("svg:text")
            .attr("text-anchor", "middle")
            .attr("dy", 14)
            .text(text)
            .style("fill-opacity", 1);
      },
      updateNode = function(node){
        node.select("text")
          .text(text);
        
        node.select("circle")
            .attr("r", 4.5);
      },
      exitNode = function(node){
        node.select("circle")
            .attr("r", 1e-6);

        node.select("text")
            .style("fill-opacity", 1e-6);
      }
    ;
  
  var connector = MindMap.elbow;

  var chart = function(selection){
    selection.each(function(root){
      var w = width - margin.left - margin.right;
      var h = height - margin.top - margin.bottom;

      var container = d3.select(this);
      var vis = container
          .attr("width", width)
          .attr("height", height)
          ;
      var graphRoot = vis.select('g');
      if(!graphRoot[0][0]){
        vis = vis.append('svg:g');
      }else{
        vis = graphRoot;
      }
      vis = vis
      .attr("transform", "translate(" + (w/2+margin.left) + "," + margin.top + ")")
      ;

      root.x0 = h / 2;
      root.y0 = 0;
      
      var tree = d3.layout.tree()
          .size([h, w]);
      
      chart.update = function() { container.transition().duration(duration).call(chart); };
      
      // Ensure we have Left and Right node lists      
      if(!(root.left || root.right)){
        var i=0, l = (root.children||[]).length;
        root.left = [];
        root.right = [];
        for(; i<l; i++){
          if(i%2){
            root.left.push(root.children[i]);
            root.children[i].position = 'left';
          }else{
            root.right.push(root.children[i]);
            root.children[i].position = 'right';
          }
        }
      }
      
      // Compute the new tree layout.
      var nodesLeft = tree
        .size([h, (w/2)-20])
        .children(function(d){
          return (d.depth===0)?d.left:d.children;
        })
        .nodes(root)
        .reverse();
      var nodesRight = tree
        .size([h, w/2])
        .children(function(d){
          return (d.depth===0)?d.right:d.children;
        })
        .nodes(root)
        .reverse();
      root.children = root.left.concat(root.right);
      var nodes = window.nodes = (function(left, right){
        var root = right[right.length-1];
        left.pop();
        left.forEach(function(node){
          node.y = -node.y;
          node.parent = root;
        });
        return left.concat(right);
      })(nodesLeft, nodesRight);

      // Update the nodes???
      var node = vis.selectAll("g.node")
          .data(nodes, function(d) { return d[identity] || (d[identity] = ++idx); });

      // Enter any new nodes at the parent's previous position.
      var nodeEnter = node.enter().append("svg:g")
          .attr("class", "node")
          .attr("transform", function(d) {
            return "translate(" + root.y0 + "," + root.x0 + ")";
          })
          .on("click", handleClick);

          
      enterNode(nodeEnter);

      // Transition nodes to their new position.
      var nodeUpdate = node.transition()
          .duration(duration)
          .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; });

    
      updateNode(nodeUpdate);

      // Transition exiting nodes to the parent's new position.
      var nodeExit = node.exit().transition()
          .duration(duration)
          .attr("transform", function() { return "translate(" + root.y + "," + root.x + ")"; })
          .remove();

      exitNode(nodeExit);

      // Update the links???
      var link = vis.selectAll("path.link")
          .data(tree.links(nodes), function(d) { return d.target[identity]; });

      // Enter any new links at the parent's previous position.
      link.enter().insert("svg:path", "g")
          .attr("class", "link")
          .attr("d", function() {
            var o = {x: root.x0, y: root.y0};
            return connector({source: o, target: o});
          })
        .transition()
          .duration(duration)
          .attr("d", connector);

      // Transition links to their new position.
      link.transition()
          .duration(duration)
          .attr("d", connector);

      // Transition exiting nodes to the parent's new position.
      link.exit().transition()
          .duration(duration)
          .attr("d", function() {
            var o = {x: root.x, y: root.y};
            return connector({source: o, target: o});
          })
          .remove();

      // Stash the old positions for transition.
      nodes.forEach(function(d) {
        d.x0 = d.x;
        d.y0 = d.y;
      });
    });
  };
  
  chart.width = function(_) {
    if (!arguments.length) return width;
    width = _;
    return chart;
  };
  
  chart.height = function(_) {
    if (!arguments.length) return height;
    height = _;
    return chart;
  };
  
  chart.duration = function(_) {
    if (!arguments.length) return duration;
    duration = _;
    return chart;
  };
  
  chart.connector = function(_) {
    if (!arguments.length) return connector;
    connector = _;
    return chart;
  };
  
  chart.click = function(_) {
    if (!arguments.length) return handleClick;
    handleClick = _;
    return chart;
  };
  
  chart.identity = function(_) {
    if (!arguments.length) return identity;
    identity = _;
    return chart;
  };
  
  chart.text = function(_) {
    if (!arguments.length) return text;
    text = _;
    return chart;
  };
  
  chart.nodeEnter = function(_){
    if (!arguments.length) return enterNode;
    enterNode = _;
    return chart;
  };
  
  chart.nodeUpdate = function(_){
    if (!arguments.length) return updateNode;
    updateNode = _;
    return chart;
  };
  
  chart.nodeExit = function(_){
    if (!arguments.length) return exitNode;
    exitNode = _;
    return chart;
  };
  
  chart.margin = function(_) {
    if (!arguments.length) return margin;
    margin.top    = typeof _.top    != 'undefined' ? _.top    : margin.top;
    margin.right  = typeof _.right  != 'undefined' ? _.right  : margin.right;
    margin.bottom = typeof _.bottom != 'undefined' ? _.bottom : margin.bottom;
    margin.left   = typeof _.left   != 'undefined' ? _.left   : margin.left;
    return chart;
  };
  
  return chart;
};

MindMap.elbow = function (d){
  var source = d.source;
  var target = d.target;
  var hy = (target.y-source.y)/2;
  return "M" + source.y + "," + source.x +
         "H" + (source.y+hy) +
         "V" + target.x + "H" + target.y;
};

MindMap.loadFreeMind = function(fileName, callback){
  d3.xml(fileName, 'application/xml', function(err, xml){
    // Changes XML to JSON
    var xmlToJson = function(xml) {
      
      // Create the return object
      var obj = {};

      if (xml.nodeType == 1) { // element
        // do attributes
        if (xml.attributes.length > 0) {
        obj["@attributes"] = {};
          for (var j = 0; j < xml.attributes.length; j++) {
            var attribute = xml.attributes.item(j);
            obj["@attributes"][attribute.nodeName] = attribute.nodeValue;
          }
        }
      } else if (xml.nodeType == 3) { // text
        obj = xml.nodeValue;
      }

      // do children
      if (xml.hasChildNodes()) {
        for(var i = 0; i < xml.childNodes.length; i++) {
          var item = xml.childNodes.item(i);
          var nodeName = item.nodeName;
          if (typeof(obj[nodeName]) == "undefined") {
            obj[nodeName] = xmlToJson(item);
          } else {
            if (typeof(obj[nodeName].push) == "undefined") {
              var old = obj[nodeName];
              obj[nodeName] = [];
              obj[nodeName].push(old);
            }
            obj[nodeName].push(xmlToJson(item));
          }
        }
      }
      return obj;
    };
    var js = xmlToJson(xml);
    var data = js.map.node;
    var parseData = function(data, direction){
      var key, i, l, dir = direction, node = {}, child;
      for(key in data['@attributes']){
        node[key.toLowerCase()] = data['@attributes'][key];
      }
      node.direction = node.direction || dir;
      l = (data.node || []).length;
      if(l){
        node.children = [];
        for(i=0; i<l; i++){
          dir = data.node[i]['@attributes'].POSITION || dir;
          child = parseData(data.node[i], {}, dir);
          (node[dir] = node[dir] || []).push(child);
          node.children.push(child);
        }
      }
      return node;
    };
    var root = parseData(data, 'right');
    
    return callback(err, root);
  });
};


// ================================================
 var getDims = function(){
        var w=window,d=document,e=d.documentElement,g=d.getElementsByTagName('body')[0],x=w.innerWidth||e.clientWidth||g.clientWidth,y=w.innerHeight||e.clientHeight||g.clientHeight;
        return {width: x, height: y};
      };
      var dims = getDims();
      var chart = MindMap()
        .width(dims.width)
        .height(dims.height-10)
        .text(function(d){
          return d.name || d.text;
        })
        .click(function(d){
          console.log(d._id);
          // Find previously selected, unselect
          d3.select(".selected").classed("selected", false);
          // Select current item
          d3.select(this).classed("selected", true);
        })
        ;
      
      var loadJSON = function(fileName){
        d3.json("/data/"+fileName, function(json) {
          var i=0, l=json.children.length;
          var root = json;
          
          json.left = [];
          json.right = [];
          for(; i<l; i++){
            if(i%2){
              json.left.push(json.children[i]);
              json.children[i].position = 'left';
            }else{
              json.right.push(json.children[i]);
              json.children[i].position = 'right';
            }
          }

          update(root);
        });
      };
      
      var loadFreeMind = function(fileName){
        MindMap.loadFreeMind('data/'+fileName, function(err, data){
          update(data);
        });
      };
      
      var update = function(data){
        window.data = data;
        d3.select('#chart')
          .datum(data)
          .call(chart)
          ;
      };
        
      var pushTopToBottom = function(){
        if(data.right[0]){
          if(data.right[0].children){
            data.right[0].children.push(data.right[0].children.shift());
          }else{
            data.right.push(data.right.shift());
          }
        }
        chart.update();
      };
      
      var addNodes = function(){
        if(data.right){
          if(data.right[0]){
            (data.right[0].children = data.right[0].children || []).push({name: 'test', children: [{name: 'Foo'}, {name: 'Bar'}, {name: 'None'}]});
          }else{
            data.right.push({name: 'test', children: [{name: 'Foo'}, {name: 'Bar'}, {name: 'None'}]});
          }
        }else{
          data.right = [{name: 'test', children: [{name: 'Foo'}, {name: 'Bar'}, {name: 'None'}]}];
        }
        chart.update();
      };
      
      var swapLeftRight = function(){
        var tmp = data.left;
        data.left = data.right;
        data.right = tmp;
        chart.update();
      };
      
      var moveNode = function(from, to){
        var n = data[from].shift();
        if(n){
          data[to].push(n);
        }
        chart.update();
      };
      
      update({
        "name": "Root",
        "children": [
          {
            "name": "Branch 1",
            "children": [
              {"name": "Leaf 3"},
              {"name": "Leaf 4"}
            ]
          },
          {"name": "Branch 2"}
        ]
      });