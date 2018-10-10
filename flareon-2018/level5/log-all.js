/*
 * User-facing API for dynamic analyses.
 */

result = ''

Wasabi.analysis = {
    binary(location, op, first, second, r) {
        if (op == 'i32.eq' && location['func'] == 47) {
            result += String.fromCharCode(first);
            console.log(location, op, "first =", first, " second =", second, "result =", r);
            console.log(result);
        }
    }
};
