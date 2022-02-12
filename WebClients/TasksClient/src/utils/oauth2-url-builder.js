export class Oauth2UrlBuilder {

    constructor() {
        this.path = "";
        this.params = {};
    }

    addPathSegment(segment) {
        if (this.path) {
            this.path += "/";
        }
        this.path += segment;
        return this;
    }

    addParam(name, value) {
        this.params[name] = value;
        return this;
    }

    addClientIdParam(value) {
        this.params["client_id"] = value;
        return this;
    }

    addRedirectUrlParam(value) {
        this.params["redirect_url"] = value;
        return this;
    }

    addScopeParam(value) {
        this.params["scope"] = value.join(",")
        return this;
    }

    build() {
        let url = this.path;
        if (Object.keys(this.params).length > 0) {
            url += "?";
            for (const key in this.params) {
                url += key;
                url += "=";
                url += this.params[key];
                url += "&";
            }
        }

        if (url.charAt(url.length - 1) === '&') {
            url = url.substr(0, url.length - 1);
        }

        return url;
    }
}