var requestInterceptor = {

    verbose : function requestInterceptor(req, res, next) {
        var info = {
            method: req.method,
            path: req.path,
            host: req.headers['host'],
            body: req.body
        };

        console.info(Date(), '-- verbose -> ', info);
        next();
    }

}

module.exports = requestInterceptor;

