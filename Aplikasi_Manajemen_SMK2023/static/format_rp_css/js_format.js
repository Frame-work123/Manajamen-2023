// JavaScript Document
$(document).ready(function(){

    // Format mata uang.
    $( '.uang' ).mask('0.000.000.000', {reverse: true});

    // Format nomor HP.
    $( '.no_hp' ).mask('0000-0000-0000');

    // Format tahun pelajaran.
    $( '.tapel' ).mask('0000/0000');
})