function addScript(src) {
    return new Promise((resolve, reject) => {
        const s = document.createElement('script');

        s.setAttribute('src', src);
        s.addEventListener('load', resolve);
        s.addEventListener('error', reject);

        document.body.appendChild(s);
    });
}


// window.onload = function () {
//     document.querySelectorAll("script").forEach(x => {
//         console.log(x);
//         // if(!x.src) 
//         document.body.removeChild(x)
//     });



//     // Build a system
//     const ui = SwaggerUIBundle({
//         version: "3.1.6",
//         urls: [
//             { url: "/swagger.json", name: "V1" },
//             { url: "/swagger.json", name: "V2" },
//         ],
//         "urls.primaryName": "V1",
//         dom_id: '#swagger-ui',
//         deepLinking: true,
//         presets: [
//             SwaggerUIBundle.presets.apis,
//             SwaggerUIStandalonePreset
//         ],
//         plugins: [
//             SwaggerUIBundle.plugins.DownloadUrl
//         ],
//         layout: "StandaloneLayout",
//         supportedSubmitMethods: []
//     })

//     window.ui = ui
// }


// import {version} from "https://cdnjs.cloudflare.com/ajax/libs/vue/3.0.5/vue.esm-browser.js";
// console.log(version);


// var swaggerUIBundle = document.createElement('script');
// swaggerUIBundle.setAttribute('src', './static/swagger-ui-bundle.js');
// document.head.appendChild(swaggerUIBundle);

// var swaggerUIStandalonePreset = document.createElement('script');
// swaggerUIStandalonePreset.setAttribute('src', './static/swagger-ui-standalone-preset.js');
// document.head.appendChild(swaggerUIStandalonePreset);


(async function main() {
    try {
        await addScript('./static/swagger-ui-bundle.js');
        await addScript('./static/swagger-ui-standalone-preset.js');

        const ui = SwaggerUIBundle({
            version: "3.1.6",
            urls: [
                { url: "/swagger.json", name: "V1" },
                { url: "/swagger.json", name: "V2" },
            ],
            "urls.primaryName": "V1",
            dom_id: '#swagger-ui',
            deepLinking: true,
            presets: [
                SwaggerUIBundle.presets.apis,
                SwaggerUIStandalonePreset
            ],
            plugins: [
                SwaggerUIBundle.plugins.DownloadUrl
            ],
            layout: "StandaloneLayout",
            supportedSubmitMethods: []
        })

        window.ui = ui
    } catch (e) {
        console.log(e);
    }
})();



