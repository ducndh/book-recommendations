/*
 * @Author: Tianyi Lu
 * @Description: 
 * @Date: 2021-03-16 01:10:29
 * @LastEditors: Tianyi Lu
 * @LastEditTime: 2021-03-16 01:11:27
 */

export function renderStars(average_rate) {
    var result = ''
    var numStars = parseInt(average_rate)
    for (var k = 0; k < numStars; k++) {
        result += '<span class="fa fa-star checked"></span>'
    }

    for (var k = 0; k < (5-numStars); k++) {
        result += '<span class="fa fa-star"></span>'
    }

    return result   
}