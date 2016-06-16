// CodeMirror, copyright (c) by Marijn Haverbeke and others
// Distributed under an MIT license: http://codemirror.net/LICENSE
//
// This lexer is used to highlight code from the dotreg
// register language.

(function(mod) {
  if (typeof exports == "object" && typeof module == "object") // CommonJS
    mod(require("../../lib/codemirror"), require("../../addon/mode/simple"));
  else if (typeof define == "function" && define.amd) // AMD
    define(["../../lib/codemirror", "../../addon/mode/simple"], mod);
  else // Plain browser env
    mod(CodeMirror);
})(function(CodeMirror) {
"use strict";

  // Word boundaries used by auto-completion
  var WORD = /[@-\w$]+/, RANGE = 500;
 
  // The list of dotreg keywords that can be used with
  // code completion
  var keyword_list = (
    // Registers
    "register endRegister " +
    "addressWidth "
    );

  // These are snippets that get expanded by code completion into pre-canned
  // blocks of code.
  var snippet_list = ("$bitfield $copy $header $bcmt $btable $bencode $bnote $register $rcmt")
  var snippet_data = {};
   

  // Code Blocks
  var today = new Date();
  var year = today.getFullYear();
  var day = today.getDate();
  var months = new Array('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec');
  var month = months[today.getMonth()];
  var created = month + "-" + day + "-" + year;

  snippet_data["$copy"]   = "# $Id$\n" +
                            "#------------------------------------------------------------------------------\n" +
                            "#\n" +
                            "#                            Inphi Corporation\n" +
                            "#                            Copyright(C) " + year  + " by Inphi Corporation\n" +
                            "#                            All rights reserved\n" +
                            "#\n" +
                            "# This document contains proprietary data and is not to be used, copied, rep-\n" +
                            "# roduced, stored in a retrieval system, transmitted, distributed or divulged\n" +
                            "# to unauthorized persons in whole or in part, without proper authorization\n" +
                            "# from Inphi Corporation. This information is the property of\n" +
                            "# Inphi Corporation with all rights reserved.\n" +
                            "#------------------------------------------------------------------------------\n" +
                            "# Title         : Register Block Title\n" +
                            "# File          : file name\n" +
                            "# Author(s)     : Author\n" +
                            "# Email         : Email\n" +
                            "# Project       : Project\n" +
                            "# Creation Date : " + created + "\n" +
                            "#\n" +
                            "#------------------------------------------------------------------------------\n" +
                            "# Description : Register map file.\n" +
                            "#\n" +
                            "#------------------------------------------------------------------------------\n" +
                            "# Revision of last commit : $Revision$\n" +
                            "# Author of last commit   : $Author$\n" +
                            "# Date of last commit     : $Date$\n" +
                            "#------------------------------------------------------------------------------\n\n";

  snippet_data["$header"] = "##############################################################\n" +
                            "addressWidth 12\n" +
                            "dataWidth 16\n" +
                            "prefix REGBLOCK\n" +
                            "referencePrefix parent_block\n" +
                            "##############################################################\n";

  snippet_data["$bitfield"] = "# Bitfield name\n" +
                              "bitfield [15:0] name sample 16'b0000000000000000\n" +
                              "attr access_code=WO\n" +
                              "bitfieldComment\n" +
                              "...\n" +
                              "endComment\n";

  snippet_data["$bcmt"] = "bitfieldComment\n" +
                          "...\n" +
                          "endComment\n";

  snippet_data["$bencode"] = "bitfieldEncoding 2'b01 DIV_BY_1 \"divide by 1\"\n" +
                             "bitfieldEncoding 2'b10 DIV_BY_2 \"divide by 2\"\n" +
                             "bitfieldEncoding 2'b11 DIV_BY_4 \"divide by 4\"\n";

  snippet_data["$bnote"]  = "bitfieldNotes 2'b00, Test 1\n" +
                            "bitfieldNotes 2'b01, Test 2\n" +
                            "bitfieldNotes 2'b10, Test 3\n" +
                            "bitfieldNotes 2'b11, Test 4\n";
                           
  snippet_data["$btable"] = "bitfieldTable Value, Description\n" +
                            "bitfieldTable 2'd0 , Value 0\n" +
                            "bitfieldTable 2'b1 , Value 1\n" +
                            "bitfieldTable 2'b2 , Value 2\n" +
                            "bitfieldTable 2'b3 , Value 3\n";

  snippet_data["$register"] = "# ...\n" +
                              "register REGNAME 16'b0\n\n" +
                              "registerComment\n" +
                              "...\n" +
                              "endComment\n\n" +
                              "bitfield [15:0] bname\n\n" +
                              "bitfieldComment\n" +
                              "endComment\n\n" +
                              "endRegister\n";
  
  snippet_data["$rcmt"] = "registerComment\n" +
                          "...\n" +
                          "endComment\n";

  var keywords = keyword_list.split(" "); 
  var snippets = snippet_list.split(" ");

  // The styles associated with language elements
  var styles = {};
  styles["tag"]                   = "keyword";
  styles["comment"]               = "comment";
  styles["keyword"] = "keyword"; 
  styles["bitfield"] = "bitfield";
  styles["register"] = "register";
  styles["comment-block"] = "comment-block";
  styles["comment-body"] = "comment-body";
  styles["bitfield-table"] = "variable-2";

  CodeMirror.defineSimpleMode("dotreg",{
    start: [
        {regex: /#/, token: styles["comment"], next: "comment"},
        {regex: /(addressWidth|dataWidth|prefix|referencePrefix|splitEndian|repeat|endRepeat)/i,    token: styles["keyword"], sol:true},
        {regex: /register/,    token: styles["register"], next: "register", sol:true},
        {regex: /./},
    ],

    comment: [
        {regex: /.$/, token: styles["comment"], next: "start"},
        {regex: /./,  token: styles["comment"]},
    ],

    // Manage the styling of registers
    register: [
        
        {regex: /#/, token: styles["comment"], next: "comment_in_register"},
        
        {regex: /(attribute|attr|name)/,  token: styles["keyword"]},

        // Check for comments
        {regex: /registerComment/i, token: styles["comment-block"], next: "register_comment", sol:true},
        
        // Check for bitfields
        {regex: /bitfield/, token: styles["bitfield"], next: "bitfield", sol:true},

        // If we hit endRegister then it is the end of the register
        {regex: /endRegister/i, token: "register", next: "start"},
        
        {regex: /./,  token: styles["register"]},
    ],
    
    comment_in_register: [
        {regex: /.$/, token: styles["comment"], next: "register"},
        {regex: /./,  token: styles["comment"]},
    ],

    // Manage the styling of bitfields
    bitfield: [
        {regex: /#/, token: styles["comment"], next: "comment_in_bitfield"},
        {regex: /(attribute|attr)/,  token: styles["keyword"]},

        // Check for comments
        {regex: /bitfieldComment/i, token: styles["comment-block"], next: "bitfield_comment", sol:true},

        // Check for tables
        {regex: /bitfieldTable/i, token: styles["bitfield-table"], next: "bitfield_table", sol:true},
        {regex: /bitfieldEncoding/i, token: styles["bitfield-table"], next: "bitfield_table", sol:true},
        {regex: /bitfieldNotes/i, token: styles["bitfield-table"], next: "bitfield_table", sol:true},
        
        {regex: /endBitfield/i, token: styles["bitfield"], next: "register", sol:true},
        
        // If we hit endRegister then it is the end of the register and bitfield
        {regex: /endRegister/i, token: styles["register"], next: "start", sol:true},
        
        {regex: /./,  token: styles["bitfield"]},
    ],
    comment_in_bitfield: [
        {regex: /.$/, token: styles["comment"], next: "bitfield"},
        {regex: /./,  token: styles["comment"]},
    ],
    
    // We're in a bitfield comment
    bitfield_comment: [
        {regex: /endComment/i, token: styles["comment-block"], next: "bitfield"},
        {regex: /.*/,  token: styles["comment-body"]}
    ],
    
    // We're in a bitfield comment
    bitfield_table: [
        {regex: /.$/i, token: styles["bitfield-table"], next: "bitfield"},
        {regex: /./,  token: styles["bitfield-table"]}
    ],

    // We're in a register comment
    register_comment: [
        {regex: /endComment/i, token: styles["comment-block"], next: "register"},
        {regex: /.*/,  token: styles["comment-body"]}
    ],


});

  
  CodeMirror.registerHelper("hint", "dotreg", function(editor, options) {
    var word = options && options.word || WORD;
    var range = options && options.range || RANGE;
    var cur = editor.getCursor(), curLine = editor.getLine(cur.line);
    var end = cur.ch, start = end;

    while (start && word.test(curLine.charAt(start - 1))) --start;
    var curWord = start != end && curLine.slice(start, end);

    var list = options && options.list || [], seen = {};
    
    // Expand any snippet templates
    if(curWord.slice(0,1) == "$") {
        // If just the $ is active the pop up the list
        // of available snippets as a reminder
        if(curWord == "$") {
            for(var i = 0; i < snippets.length; i++) {
                list.push(snippets[i]);
            }
        }
        else {
            for(var i = 0; i < snippets.length; i++) {
                var idx = snippets[i].indexOf(curWord);
                if(idx == 0) {
                    var snippet_name = snippets[i];
                    var snippet_value = snippet_data[snippet_name];
                    list.push(snippet_value);
                    //seen[snippet_name] = true;
                }
            }
        }
    } 
    // Scan the list of keywords for matches first
    for(var i = 0; i < keywords.length; i++) {
        var idx = keywords[i].indexOf(curWord);
        if(idx == 0) {
            list.push(keywords[i]);
            seen[keywords[i]] = true;
        }
    }

    // After that search for anything instantiated in the
    // document.
    var re = new RegExp(word.source, "g");
    for (var dir = -1; dir <= 1; dir += 2) {
      var line = cur.line, endLine = Math.min(Math.max(line + dir * range, editor.firstLine()), editor.lastLine()) + dir;
      for (; line != endLine; line += dir) {
        var text = editor.getLine(line), m;
        while (m = re.exec(text)) {
          if (line == cur.line && m[0] === curWord) continue;
          if ((!curWord || m[0].lastIndexOf(curWord, 0) == 0) && !Object.prototype.hasOwnProperty.call(seen, m[0])) {
            seen[m[0]] = true;
            list.push(m[0]);
          }
        }
      }
    }
    return {list: list, from: CodeMirror.Pos(cur.line, start), to: CodeMirror.Pos(cur.line, end)};
  });
  
CodeMirror.defineMIME("text/dotreg", "dotreg");

});
