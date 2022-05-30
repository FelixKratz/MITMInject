var System = {};

System.callInjectorAPI = function(command, callback) {
    System.callAjax("injectorAPI/", command, callback);
};

System.callAjax = function(url, command, callback) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function(){
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200){
            callback(xmlhttp.response);
        }
    }
    xmlhttp.open("POST", url, true);
    xmlhttp.send(command);
}

System.awaitHtmlElement = function(selector, callback, disconnect = false, context=document) {
    new MutationObserver(
      (mutations, observer) => {
        for (i = 0; i < selector.length; i++) {
            if (!context.querySelector(selector[i])) return;
        }
        callback(context.querySelector(selector[0]));
        if (disconnect) observer.disconnect();
    }).observe(context.documentElement, {
        childList: true, subtree: true, attributes: false, characterData: false});
};

System.removeHTMLElement = function(element) {
    if (element && element.parentNode)
       element.parentNode.removeChild(element);
};

System.addEventHandler = function(element, handler, type) {
    element.addEventListener(type, handler);
};

System.removeEventHandlerFromElement = function(element, type) {
    element.removeEventListener(type);
};

System.removeAllEventHandlersFromElement = function(element) {
    elementClone = element.cloneNode(true);
    element.parentNode.replaceChild(elementClone, element);
    return elementClone
};

System.prunePaths = []

System.pushJSONParseProxy = function(_prunePaths = "") {
    System.prunePaths.push(...(_prunePaths !== '' ? _prunePaths.split(/ +/) : []));
}

System.monitorJSON = false

// *** Stolen straight from uBlock with slight modifications ***
const findOwner = function(root, path) {
    let owner = root;
    let chain = path;
    for (;;) {
        if (owner instanceof Object === false) { return; }
        const pos = chain.indexOf('.');
        if (pos === -1) {
            return owner.hasOwnProperty(chain) ? [ owner, chain ] : undefined;
        }
        const prop = chain.slice(0, pos);
        if (owner.hasOwnProperty(prop) === false) { return; }
        owner = owner[prop];
        chain = chain.slice(pos + 1);
    }
};

JSON.parse = new Proxy(JSON.parse, {
    apply: function() {
        if (System.monitorJSON) {
            System.callInjectorAPI(...arguments, undefined)
        }
        const r = Reflect.apply(...arguments);
        if (System.prunePaths.length === 0) { 
            return r; 
        }
        for (const path of System.prunePaths) {
            const details = findOwner(r, path);
            if (details !== undefined) { 
                delete details[0][details[1]]; 
            }
        }

        return r;
    },
});
