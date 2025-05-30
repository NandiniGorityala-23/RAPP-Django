/**
 * All auto suggestion boxes are fucked up or badly written.
 * This is an attempt to create something that doesn't suck...
 *
 * Requires: jQuery
 *
 * Author: Nicolas Bize
 * Date: Feb. 8th 2013
 * Version: 1.3.1
 * Licence: TagSuggest is licenced under MIT licence (https://www.opensource.org/licenses/mit-license.php)
 */
$(function($)
{
    "use strict";
    var TagSuggest = function(element, options)
    {
        var ms = this;
        var defaults = {
            allowFreeEntries: true,
            cls: '',
            data: null,
            dataUrlParams: {},
            disabled: false,
            displayField: 'name',
            editable: true,
            emptyText: function() {
                return cfg.editable ? 'Type or click here' : 'Click here';
            },
            emptyTextCls: 'tag-empty-text',
            expanded: false,
            expandOnFocus: function() {
                return cfg.editable ? false : true;
            },
            groupBy: null,
            hideTrigger: false,
            highlight: true,
            id: function() {
                return 'tag-ctn-' + $('div[id^="tag-ctn"]').length;
            },
            infoMsgCls: '',
            inputCfg: {},
            invalidCls: 'tag-ctn-invalid',
            matchCase: false,
            maxDropHeight: 290,
            maxEntryLength: null,
            maxEntryRenderer: function(v) {
                return 'Please reduce your entry by ' + v + ' character' + (v > 1 ? 's':'');
            },
            maxSuggestions: null,
            maxSelection: 10,
            maxSelectionRenderer: function(v) {
                return 'You cannot choose more than ' + v + ' item' + (v > 1 ? 's':'');
            },
            method: 'POST',
            minChars: 0,
            minCharsRenderer: function(v) {
                return 'Please type ' + v + ' more character' + (v > 1 ? 's':'');
            },
            name: null,
            noSuggestionText: 'No suggestions',
            preselectSingleSuggestion: true,
            renderer: null,
            required: false,
            resultAsString: false,
            resultsField: 'results',
            selectionCls: '',
            selectionPosition: 'inner',
            selectionRenderer: null,
            selectionStacked: false,
            sortDir: 'asc',
            sortOrder: null,
            strictSuggest: false,
            style: '',
            toggleOnClick: false,
            typeDelay: 400,
            useTabKey: false,
            useCommaKey: true,
            useZebraStyle: true,
            value: null,
            valueField: 'id'
        };

        var conf = $.extend({},options);
        var cfg = $.extend(true, {}, defaults, conf);

        //some init stuff
        if ($.isFunction(cfg.emptyText)) {
            cfg.emptyText = cfg.emptyText.call(this);
        }
        if ($.isFunction(cfg.expandOnFocus)) {
            cfg.expandOnFocus = cfg.expandOnFocus.call(this);
        }
        if ($.isFunction(cfg.id)) {
            cfg.id = cfg.id.call(this);
        }

        /**********  PUBLIC METHODS ************/
        /**
         * Add one or multiple json items to the current selection
         * @param items - json object or array of json objects
         * @param isSilent - (optional) set to true to suppress 'selectionchange' event from being triggered
         */
        this.addToSelection = function(items, isSilent)
        {
            if (!cfg.maxSelection || _selection.length < cfg.maxSelection) {
                if (!$.isArray(items)) {
                    items = [items];
                }
                var valuechanged = false;
                $.each(items, function(index, json) {
                    if ($.inArray(json[cfg.valueField], ms.getValue()) === -1) {
                        _selection.push(json);
                        valuechanged = true;
                    }
                });
                if(valuechanged === true) {
                    self._renderSelection();
                    this.empty();
                    if (isSilent !== true) {
                        $(this).trigger('selectionchange', [this, this.getSelectedItems()]);
                    }
                }
            }
        };

        /**
         * Clears the current selection
         * @param isSilent - (optional) set to true to suppress 'selectionchange' event from being triggered
         */
        this.clear = function(isSilent)
        {
            this.removeFromSelection(_selection.slice(0), isSilent); //clone array to avoid concurrency issues
        };

        /**
         * Collapse the drop down part of the combo
         */
        this.collapse = function()
        {
            if (cfg.expanded === true) {
                this.combobox.detach();
                cfg.expanded = false;
                $(this).trigger('collapse', [this]);
            }
        };

        /**
         * Set the component in a disabled state.
         */
        this.disable = function()
        {
            this.container.addClass('tag-ctn-disabled');
            cfg.disabled = true;
            ms.input.attr('disabled', true);
        };

        /**
         * Empties out the combo user text
         */
        this.empty = function(){
            this.input.removeClass(cfg.emptyTextCls);
            this.input.val('');
        };

        /**
         * Set the component in a enable state.
         */
        this.enable = function()
        {
            this.container.removeClass('tag-ctn-disabled');
            cfg.disabled = false;
            ms.input.attr('disabled', false);
        };

        /**
         * Expand the drop drown part of the combo.
         */
        this.expand = function()
        {
            if (!cfg.expanded && (this.input.val().length >= cfg.minChars || this.combobox.children().size() > 0)) {
                this.combobox.appendTo(this.container);
                self._processSuggestions();
                cfg.expanded = true;
                $(this).trigger('expand', [this]);
            }
        };

        /**
         * Retrieve component enabled status
         */
        this.isDisabled = function()
        {
            return cfg.disabled;
        };

        /**
         * Checks whether the field is valid or not
         * @return {boolean}
         */
        this.isValid = function()
        {
            return cfg.required === false || _selection.length > 0;
        };

        /**
         * Gets the data params for current ajax request
         */
        this.getDataUrlParams = function()
        {
            return cfg.dataUrlParams;
        };

        /**
         * Gets the name given to the form input
         */
        this.getName = function()
        {
            return cfg.name;
        };

        /**
         * Retrieve an array of selected json objects
         * @return {Array}
         */
        this.getSelectedItems = function()
        {
            return _selection;
        };

        /**
         * Retrieve the current text entered by the user
         */
        this.getRawValue = function(){
            return ms.input.val() !== cfg.emptyText ? ms.input.val() : '';
        };

        /**
         * Retrieve an array of selected values
         */
        this.getValue = function()
        {
            return $.map(_selection, function(o) {
                return o[cfg.valueField];
            });
        };

        /**
         * Remove one or multiples json items from the current selection
         * @param items - json object or array of json objects
         * @param isSilent - (optional) set to true to suppress 'selectionchange' event from being triggered
         */
        this.removeFromSelection = function(items, isSilent)
        {
            if (!$.isArray(items)) {
                items = [items];
            }
            var valuechanged = false;
            $.each(items, function(index, json) {
                var i = $.inArray(json[cfg.valueField], ms.getValue());
                if (i > -1) {
                    _selection.splice(i, 1);
                    valuechanged = true;
                }
            });
            if (valuechanged === true) {
                self._renderSelection();
                if(isSilent !== true){
                    $(this).trigger('selectionchange', [this, this.getSelectedItems()]);
                }
                if(cfg.expandOnFocus){
                    ms.expand();
                }
                if(cfg.expanded) {
                    self._processSuggestions();
                }
            }
        };

        /**
         * Set up some combo data after it has been rendered
         * @param data
         */
        this.setData = function(data){
            cfg.data = data;
            self._processSuggestions();
        };

        /**
         * Sets the name for the input field so it can be fetched in the form
         * @param name
         */
        this.setName = function(name){
            cfg.name = name;
            if(ms._valueContainer){
                ms._valueContainer.name = name;
            }
        };

        /**
         * Sets a value for the combo box. Value must be a value or an array of value with data type matching valueField one.
         * @param data
         */
        this.setValue = function(data)
        {
            var values = data, items = [];
            if(!$.isArray(data)){
                if(typeof(data) === 'string'){
                    if(data.indexOf('[') > -1){
                        values = eval(data);
                    } else if(data.indexOf(',') > -1){
                        values = data.split(',');
                    }
                } else {
                    values = [data];
                }
            }

            $.each(_cbData, function(index, obj) {
                if($.inArray(obj[cfg.valueField], values) > -1) {
                    items.push(obj);
                }
            });
            if(items.length > 0) {
                this.addToSelection(items);
            }
        };

        /**
         * Sets data params for subsequent ajax requests
         * @param params
         */
        this.setDataUrlParams = function(params)
        {
            cfg.dataUrlParams = $.extend({},params);
        };

        /**********  PRIVATE ************/
        var _selection = [],      // selected objects
            _comboItemHeight = 0, // height for each combo item.
            _timer,
            _hasFocus = false,
            _groups = null,
            _cbData = [],
            _ctrlDown = false;

        var self = {

            /**
             * Empties the result container and refills it with the array of json results in input
             * @private
             */
            _displaySuggestions: function(data) {
                ms.combobox.empty();

                var resHeight = 0,//total height taken by displayed results.
                    nbGroups = 0;

                if(_groups === null) {
                    self._renderComboItems(data);
                    resHeight = _comboItemHeight * data.length;
                }
                else {
                    for(var grpName in _groups) {
                        nbGroups += 1;
                        $('<div/>', {
                            'class': 'tag-res-group',
                            html: grpName
                        }).appendTo(ms.combobox);
                        self._renderComboItems(_groups[grpName].items, true);
                    }
                    resHeight = _comboItemHeight * (data.length + nbGroups);
                }

                if(resHeight < ms.combobox.height() || resHeight <= cfg.maxDropHeight) {
                    ms.combobox.height(resHeight);
                }
                else if(resHeight >= ms.combobox.height() && resHeight > cfg.maxDropHeight) {
                    ms.combobox.height(cfg.maxDropHeight);
                }

                if(data.length === 1 && cfg.preselectSingleSuggestion === true) {
                    ms.combobox.children().filter(':last').addClass('tag-res-item-active');
                }

                if(data.length === 0 && ms.getRawValue() !== "") {
                    self._updateHelper(cfg.noSuggestionText);
                    ms.collapse();
                }
            },

            /**
             * Returns an array of json objects from an array of strings.
             * @private
             */
            _getEntriesFromStringArray: function(data) {
                var json = [];
                $.each(data, function(index, s) {
                    var entry = {};
                    entry[cfg.displayField] = entry[cfg.valueField] = $.trim(s);
                    json.push(entry);
                });
                return json;
            },

            /**
             * Replaces html with highlighted html according to case
             * @param html
             * @private
             */
            _highlightSuggestion: function(html) {
                var q = ms.input.val() !== cfg.emptyText ? ms.input.val() : '';
                if(q.length === 0) {
                    return html;//nothing entered as input
                }

                if(cfg.matchCase === true) {
                    html = html.replace(new RegExp('(' + q + ')(?!([^<]+)?>)','g'), '<em>$1</em>');
                }
                else {
                    html = html.replace(new RegExp('(' + q + ')(?!([^<]+)?>)','gi'), '<em>$1</em>');
                }
                return html;
            },

            /**
             * Moves the selected cursor amongst the list item
             * @param dir - 'up' or 'down'
             * @private
             */
            _moveSelectedRow: function(dir) {
                if(!cfg.expanded) {
                    ms.expand();
                }
                var list, start, active, scrollPos;
                list = ms.combobox.find(".tag-res-item");
                if(dir === 'down') {
                    start = list.eq(0);
                }
                else {
                    start = list.filter(':last');
                }
                active = ms.combobox.find('.tag-res-item-active:first');
                if(active.length > 0) {
                    if(dir === 'down') {
                        start = active.nextAll('.tag-res-item').first();
                        if(start.length === 0) {
                            start = list.eq(0);
                        }
                        scrollPos = ms.combobox.scrollTop();
                        ms.combobox.scrollTop(0);
                        if(start[0].offsetTop + start.outerHeight() > ms.combobox.height()) {
                            ms.combobox.scrollTop(scrollPos + _comboItemHeight);
                        }
                    }
                    else {
                        start = active.prevAll('.tag-res-item').first();
                        if(start.length === 0) {
                            start = list.filter(':last');
                            ms.combobox.scrollTop(_comboItemHeight * list.length);
                        }
                        if(start[0].offsetTop < ms.combobox.scrollTop()) {
                            ms.combobox.scrollTop(ms.combobox.scrollTop() - _comboItemHeight);
                        }
                    }
                }
                list.removeClass("tag-res-item-active");
                start.addClass("tag-res-item-active");
            },

            /**
             * According to given data and query, sort and add suggestions in their container
             * @private
             */
            _processSuggestions: function(source) {
                var json = null, data = source || cfg.data;
                if(data !== null) {
                    if(typeof(data) === 'function'){
                        data = data.call(ms);
                    }
                    if(typeof(data) === 'string' && data.indexOf(',') < 0) {//get results from ajax
                        $(ms).trigger('beforeload', [ms]);
                        var params = $.extend({query: ms.input.val()}, cfg.dataUrlParams);
                        $.ajax({
                            type: cfg.method,
                            url: data,
                            data: params,
                            success: function(asyncData){
                                json = typeof(asyncData) === 'string' ? JSON.parse(asyncData) : asyncData;
                                self._processSuggestions(json);
                                $(ms).trigger('load', [ms, json]);
                            },
                            error: function(){
                                throw("Could not reach server");
                            }
                        });
                        return;
                    } else if(typeof(data) === 'string' && data.indexOf(',') > -1) {//results from csv string
                        _cbData = self._getEntriesFromStringArray(data.split(','));
                    } else {//results from local array
                        if(data.length > 0 && typeof(data[0]) === 'string') {//results from array of strings
                            _cbData = self._getEntriesFromStringArray(data);
                        } else {//regular json array or json object with results property
                            _cbData = data[cfg.resultsField] || data;
                        }
                    }
                    self._displaySuggestions(self._sortAndTrim(_cbData));

                }
            },

            /**
             * Render the component to the given input DOM element
             * @private
             */
            _render: function(el) {
                $(ms).trigger('beforerender', [ms]);
                var w = $.isFunction(cfg.width) ? cfg.width.call(el) : cfg.width;
               //holds the main div, will relay the focus events to the contained input element.
                ms.container = $('<div/>', {
                    id: cfg.id,
                    'class': 'tag-ctn auto-suggest' + cfg.cls +
                        (cfg.disabled === true ? ' tag-ctn-disabled' : '') +
                        (cfg.editable === true ? '' : ' tag-ctn-readonly'),
                    style: cfg.style
                }).width(w);
                ms.container.focus($.proxy(handlers._onFocus, this));
                ms.container.blur($.proxy(handlers._onBlur, this));
                ms.container.keydown($.proxy(handlers._onKeyDown, this));
                ms.container.keyup($.proxy(handlers._onKeyUp, this));

               //holds the input field
                ms.input = $('<input/>', $.extend({
                    id: 'tag-input-' + $('input[id^="tag-input"]').length,
                    type: 'text',
                    'class': cfg.emptyTextCls + (cfg.editable === true ? '' : ' tag-input-readonly'),
                    value: cfg.emptyText,
                    readonly: !cfg.editable,
                    disabled: cfg.disabled
                }, cfg.inputCfg)).width(w - (cfg.hideTrigger ? 16 : 42));

                ms.input.focus($.proxy(handlers._onInputFocus, this));
                ms.input.click($.proxy(handlers._onInputClick, this));

               //holds the trigger on the right side
                if(cfg.hideTrigger === false) {
                    ms.trigger = $('<div/>', {
                        id: 'tag-trigger-' + $('div[id^="tag-trigger"]').length,
                        'class': 'tag-trigger',
                        html: '<div class="tag-trigger-ico"></div>'
                    });
                    ms.trigger.click($.proxy(handlers._onTriggerClick, this));
                    ms.container.append(ms.trigger);
                }

               //holds the suggestions. will always be placed on focus
                ms.combobox = $('<div/>', {
                    id: 'tag-res-ctn-' + $('div[id^="tag-res-ctn"]').length,
                    'class': 'tag-res-ctn '
                }).width(w).height(cfg.maxDropHeight);

               //bind the onclick and mouseover using delegated events (needs jQuery >= 1.7)
                ms.combobox.on('click', 'div.tag-res-item', $.proxy(handlers._onComboItemSelected, this));
                ms.combobox.on('mouseover', 'div.tag-res-item', $.proxy(handlers._onComboItemMouseOver, this));

                ms.selectionContainer = $('<div/>', {
                    id: 'tag-sel-ctn-' +  $('div[id^="tag-sel-ctn"]').length,
                    'class': 'tag-sel-ctn'
                });
                ms.selectionContainer.click($.proxy(handlers._onFocus, this));

                if(cfg.selectionPosition === 'inner') {
                    ms.selectionContainer.append(ms.input);
                }
                else {
                    ms.container.append(ms.input);
                }

                ms.helper = $('<div/>', {
                    'class': 'tag-helper ' + cfg.infoMsgCls
                });
                self._updateHelper();
                ms.container.append(ms.helper);


               //Render the whole thing
                $(el).replaceWith(ms.container);

                switch(cfg.selectionPosition) {
                    case 'bottom':
                        ms.selectionContainer.insertAfter(ms.container);
                        if(cfg.selectionStacked === true) {
                            ms.selectionContainer.width(ms.container.width());
                            ms.selectionContainer.addClass('tag-stacked');
                        }
                        break;
                    case 'right':
                        ms.selectionContainer.insertAfter(ms.container);
                        ms.container.css('float', 'left');
                        break;
                    default:
                        ms.container.append(ms.selectionContainer);
                        break;
                }

                self._processSuggestions();
                if(cfg.value !== null) {
                    ms.setValue(cfg.value);
                    self._renderSelection();
                }

                $(ms).trigger('afterrender', [ms]);
                $("body").click(function(e) {
                    if(ms.container.hasClass('tag-ctn-bootstrap-focus') &&
                        ms.container.has(e.target).length === 0 &&
                        e.target.className.indexOf('tag-res-item') < 0 &&
                        e.target.className.indexOf('tag-close-btn') < 0 &&
                        ms.container[0] !== e.target) {
                        handlers._onBlur();
                    }
                });

                if(cfg.expanded === true) {
                    cfg.expanded = false;
                    ms.expand();
                }
            },

            _renderComboItems: function(items, isGrouped) {
                var ref = this, html = '';
                $.each(items, function(index, value) {
                    var displayed = cfg.renderer !== null ? cfg.renderer.call(ref, value) : value[cfg.displayField];
                    var resultItemEl = $('<div/>', {
                        'class': 'tag-res-item ' + (isGrouped ? 'tag-res-item-grouped ':'') +
                            (index % 2 === 1 && cfg.useZebraStyle === true ? 'tag-res-odd' : ''),
                        html: cfg.highlight === true ? self._highlightSuggestion(displayed) : displayed,
                        'data-json': JSON.stringify(value)
                    });
                    resultItemEl.click($.proxy(handlers._onComboItemSelected, ref));
                    resultItemEl.mouseover($.proxy(handlers._onComboItemMouseOver, ref));
                    html += $('<div/>').append(resultItemEl).html();
                });
                ms.combobox.append(html);
                _comboItemHeight = ms.combobox.find('.tag-res-item:first').outerHeight();
            },

            /**
             * Renders the selected items into their container.
             * @private
             */
            _renderSelection: function() {
                var ref = this, w = 0, inputOffset = 0, items = [],
                    asText = cfg.resultAsString === true && !_hasFocus;

                ms.selectionContainer.find('.tag-sel-item').remove();
                if(ms._valueContainer !== undefined) {
                    ms._valueContainer.remove();
                }

                $.each(_selection, function(index, value){

                    var selectedItemEl, delItemEl,
                        selectedItemHtml = cfg.selectionRenderer !== null ? cfg.selectionRenderer.call(ref, value) : value[cfg.displayField];
                   //tag representing selected value
                    if(asText === true) {
                        selectedItemEl = $('<div/>', {
                            'class': 'tag-sel-item tag-sel-text ' + cfg.selectionCls,
                            html: selectedItemHtml + (index === (_selection.length - 1) ? '' : ',')
                        }).data('json', value);
                    }
                    else {
                        selectedItemEl = $('<div/>', {
                            'class': 'tag-sel-item ' + cfg.selectionCls,
                            html: selectedItemHtml
                        }).data('json', value);

                        if(cfg.disabled === false){
                           //small cross img
                            delItemEl = $('<span/>', {
                                'class': 'tag-close-btn'
                            }).data('json', value).appendTo(selectedItemEl);

                            delItemEl.click($.proxy(handlers._onTagTriggerClick, ref));
                        }
                    }

                    items.push(selectedItemEl);
                });

                ms.selectionContainer.prepend(items);
                ms._valueContainer = $('<input/>', {
                    type: 'hidden',
                    name: cfg.name,
                    value: JSON.stringify(ms.getValue())
                });
                ms._valueContainer.appendTo(ms.selectionContainer);

                if(cfg.selectionPosition === 'inner') {
                    ms.input.width(0);
                    inputOffset = ms.input.offset().left - ms.selectionContainer.offset().left;
                    w = ms.container.width() - inputOffset - 42;
                    ms.input.width(w);
                    ms.container.height(ms.selectionContainer.height());
                }

                if(_selection.length === cfg.maxSelection){
                    self._updateHelper(cfg.maxSelectionRenderer.call(this, _selection.length));
                } else {
                    ms.helper.hide();
                }
            },

            /**
             * Select an item either through keyboard or mouse
             * @param item
             * @private
             */
            _selectItem: function(item) {
                if(cfg.maxSelection === 1){
                    _selection = [];
                }
                ms.addToSelection(item.data('json'));
                item.removeClass('tag-res-item-active');
                if(cfg.expandOnFocus === false || _selection.length === cfg.maxSelection){
                    ms.collapse();
                }
                if(!_hasFocus){
                    ms.input.focus();
                } else if(_hasFocus && (cfg.expandOnFocus || _ctrlDown)){
                    self._processSuggestions();
                    if(_ctrlDown){
                        ms.expand();
                    }
                }
            },

            /**
             * Sorts the results and cut them down to max//of displayed results at once
             * @private
             */
            _sortAndTrim: function(data) {
                var q = ms.getRawValue(),
                    filtered = [],
                    newSuggestions = [],
                    selectedValues = ms.getValue();
               //filter the data according to given input
                if(q.length > 0) {
                    $.each(data, function(index, obj) {
                        var name = obj[cfg.displayField];
                        if((cfg.matchCase === true && name.indexOf(q) > -1) ||
                            (cfg.matchCase === false && name.toLowerCase().indexOf(q.toLowerCase()) > -1)) {
                            if(cfg.strictSuggest === false || name.toLowerCase().indexOf(q.toLowerCase()) === 0) {
                                filtered.push(obj);
                            }
                        }
                    });
                }
                else {
                    filtered = data;
                }
               //take out the ones that have already been selected
                $.each(filtered, function(index, obj) {
                    if($.inArray(obj[cfg.valueField], selectedValues) === -1) {
                        newSuggestions.push(obj);
                    }
                });
               //sort the data
                if(cfg.sortOrder !== null) {
                    newSuggestions.sort(function(a,b) {
                        if(a[cfg.sortOrder] < b[cfg.sortOrder]) {
                            return cfg.sortDir === 'asc' ? -1 : 1;
                        }
                        if(a[cfg.sortOrder] > b[cfg.sortOrder]) {
                            return cfg.sortDir === 'asc' ? 1 : -1;
                        }
                        return 0;
                    });
                }
               //trim it down
                if(cfg.maxSuggestions && cfg.maxSuggestions > 0) {
                    newSuggestions = newSuggestions.slice(0, cfg.maxSuggestions);
                }
               //build groups
                if(cfg.groupBy !== null) {
                    _groups = {};
                    $.each(newSuggestions, function(index, value) {
                        if(_groups[value[cfg.groupBy]] === undefined) {
                            _groups[value[cfg.groupBy]] = {title: value[cfg.groupBy], items: [value]};
                        }
                        else {
                            _groups[value[cfg.groupBy]].items.push(value);
                        }
                    });
                }
                return newSuggestions;
            },

            /**
             * Update the helper text
             * @private
             */
            _updateHelper: function(html) {
                ms.helper.html(html);
                if(!ms.helper.is(":visible")) {
                    ms.helper.fadeIn();
                }
            }
        };

        var handlers = {
            /**
             * Triggered when blurring out of the component
             * @private
             */
            _onBlur: function() {
                ms.container.removeClass('tag-ctn-bootstrap-focus');
                ms.collapse();
                _hasFocus = false;
                if(ms.getRawValue() !== '' && cfg.allowFreeEntries === true){
                    var obj = {};
                    obj[cfg.displayField] = obj[cfg.valueField] = ms.getRawValue();
                    ms.addToSelection(obj);
                }
                self._renderSelection();

                if(ms.isValid() === false) {
                    ms.container.addClass('tag-ctn-invalid');
                }

                if(ms.input.val() === '' && _selection.length === 0) {
                    ms.input.addClass(cfg.emptyTextCls);
                    ms.input.val(cfg.emptyText);
                }
                else if(ms.input.val() !== '' && cfg.allowFreeEntries === false) {
                    ms.empty();
                    self._updateHelper('');
                }

                if(ms.input.is(":focus")) {
                    $(ms).trigger('blur', [ms]);
                }
            },

            /**
             * Triggered when hovering an element in the combo
             * @param e
             * @private
             */
            _onComboItemMouseOver: function(e) {
                ms.combobox.children().removeClass('tag-res-item-active');
                $(e.currentTarget).addClass('tag-res-item-active');
            },

            /**
             * Triggered when an item is chosen from the list
             * @param e
             * @private
             */
            _onComboItemSelected: function(e) {
                self._selectItem($(e.currentTarget));
            },

            /**
             * Triggered when focusing on the container div. Will focus on the input field instead.
             * @private
             */
            _onFocus: function() {
                ms.input.focus();
            },

            /**
             * Triggered when clicking on the input text field
             * @private
             */
            _onInputClick: function(){
                if (ms.isDisabled() === false && _hasFocus) {
                    if (cfg.toggleOnClick === true) {
                        if (cfg.expanded){
                            ms.collapse();
                        } else {
                            ms.expand();
                        }
                    }
                }
            },

            /**
             * Triggered when focusing on the input text field.
             * @private
             */
            _onInputFocus: function() {
                if(ms.isDisabled() === false && !_hasFocus) {
                    _hasFocus = true;
                    ms.container.addClass('tag-ctn-bootstrap-focus');
                    ms.container.removeClass(cfg.invalidCls);

                    if(ms.input.val() === cfg.emptyText) {
                        ms.empty();
                    }

                    var curLength = ms.getRawValue().length;
                    if(cfg.expandOnFocus === true){
                        ms.expand();
                    }

                    if(_selection.length === cfg.maxSelection) {
                        self._updateHelper(cfg.maxSelectionRenderer.call(this, _selection.length));
                    } else if(curLength < cfg.minChars) {
                        self._updateHelper(cfg.minCharsRenderer.call(this, cfg.minChars - curLength));
                    }

                    self._renderSelection();
                    $(ms).trigger('focus', [ms]);
                }
            },

            /**
             * Triggered when the user presses a key while the component has focus
             * This is where we want to handle all keys that don't require the user input field
             * since it hasn't registered the key hit yet
             * @param e keyEvent
             * @private
             */
            _onKeyDown: function(e) {
               //check how tab should be handled
                var active = ms.combobox.find('.tag-res-item-active:first'),
                    freeInput = ms.input.val() !== cfg.emptyText ? ms.input.val() : '';
                $(ms).trigger('keydown', [ms, e]);

                if(e.keyCode === 9 && (cfg.useTabKey === false ||
                    (cfg.useTabKey === true && active.length === 0 && ms.input.val().length === 0))) {
                    handlers._onBlur();
                    return;
                }
                switch(e.keyCode) {
                    case 8: //backspace
                        if(freeInput.length === 0 && ms.getSelectedItems().length > 0 && cfg.selectionPosition === 'inner') {
                            _selection.pop();
                            self._renderSelection();
                            $(ms).trigger('selectionchange', [ms, ms.getSelectedItems()]);
                            ms.input.focus();
                            e.preventDefault();
                        }
                        break;
                    case 9://tab
                    case 188://esc
                    case 13://enter
                        e.preventDefault();
                        break;
                    case 17://ctrl
                        _ctrlDown = true;
                        break;
                    case 40://down
                        e.preventDefault();
                        self._moveSelectedRow("down");
                        break;
                    case 38://up
                        e.preventDefault();
                        self._moveSelectedRow("up");
                        break;
                    default:
                        if(_selection.length === cfg.maxSelection) {
                            e.preventDefault();
                        }
                        break;
                }
            },

            /**
             * Triggered when a key is released while the component has focus
             * @param e
             * @private
             */
            _onKeyUp: function(e) {
                var freeInput = ms.getRawValue(),
                    inputValid = $.trim(ms.input.val()).length > 0 && ms.input.val() !== cfg.emptyText &&
                        (!cfg.maxEntryLength || $.trim(ms.input.val()).length <= cfg.maxEntryLength),
                    selected,
                    obj = {};

                $(ms).trigger('keyup', [ms, e]);

                clearTimeout(_timer);

               //collapse if escape, but keep focus.
                if(e.keyCode === 27 && cfg.expanded) {
                    ms.combobox.height(0);
                }
               //ignore a bunch of keys
                if((e.keyCode === 9 && cfg.useTabKey === false) || (e.keyCode > 13 && e.keyCode < 32)) {
                    if(e.keyCode === 17){
                        _ctrlDown = false;
                    }
                    return;
                }
                switch(e.keyCode) {
                    case 40:case 38://up, down
                    e.preventDefault();
                    break;
                    case 13:case 9:case 188:// enter, tab, comma
                    if(e.keyCode !== 188 || cfg.useCommaKey === true) {
                        e.preventDefault();
                        if(cfg.expanded === true){//if a selection is performed, select it and reset field
                            selected = ms.combobox.find('.tag-res-item-active:first');
                            if(selected.length > 0) {
                                self._selectItem(selected);
                                return;
                            }
                        }
                       //if no selection or if freetext entered and free entries allowed, add new obj to selection
                        if(inputValid === true && cfg.allowFreeEntries === true) {
                            obj[cfg.displayField] = obj[cfg.valueField] = freeInput;
                            ms.addToSelection(obj);
                            ms.collapse();//reset combo suggestions
                            ms.input.focus();
                        }
                        break;
                    }
                    default:
                        if(_selection.length === cfg.maxSelection){
                            self._updateHelper(cfg.maxSelectionRenderer.call(this, _selection.length));
                        }
                        else {
                            if(freeInput.length < cfg.minChars) {
                                self._updateHelper(cfg.minCharsRenderer.call(this, cfg.minChars - freeInput.length));
                                if(cfg.expanded === true) {
                                    ms.collapse();
                                }
                            }
                            else if(cfg.maxEntryLength && freeInput.length > cfg.maxEntryLength) {
                                self._updateHelper(cfg.maxEntryRenderer.call(this, freeInput.length - cfg.maxEntryLength));
                                if(cfg.expanded === true) {
                                    ms.collapse();
                                }
                            }
                            else {
                                ms.helper.hide();
                                if(cfg.minChars <= freeInput.length){
                                    _timer = setTimeout(function() {
                                        if(cfg.expanded === true) {
                                            self._processSuggestions();
                                        } else {
                                            ms.expand();
                                        }
                                    }, cfg.typeDelay);
                                }
                            }
                        }
                        break;
                }
            },

            /**
             * Triggered when clicking upon cross for deletion
             * @param e
             * @private
             */
            _onTagTriggerClick: function(e) {
                ms.removeFromSelection($(e.currentTarget).data('json'));
            },

            /**
             * Triggered when clicking on the small trigger in the right
             * @private
             */
            _onTriggerClick: function() {
                if(ms.isDisabled() === false && !(cfg.expandOnFocus === true && _selection.length === cfg.maxSelection)) {
                    $(ms).trigger('triggerclick', [ms]);
                    if(cfg.expanded === true) {
                        ms.collapse();
                    } else {
                        var curLength = ms.getRawValue().length;
                        if(curLength >= cfg.minChars){
                            ms.input.focus();
                            ms.expand();
                        } else {
                            self._updateHelper(cfg.minCharsRenderer.call(this, cfg.minChars - curLength));
                        }
                    }
                }
            }
        };

       //startup point
        if(element !== null) {
            self._render(element);
        }
    };

    $.fn.tagSuggest = function(options) {
        var obj = $(this);

        if(obj.size() === 1 && obj.data('tagSuggest')) {
            return obj.data('tagSuggest');
        }

        obj.each(function(i) {
            // assume $(this) is an element
            var cntr = $(this);

            // Return early if this element already has a plugin instance
            if(cntr.data('tagSuggest')){
                return;
            }

            if(this.nodeName.toLowerCase() === 'select'){ // rendering from select
                options.data = [];
                options.value = [];
                $.each(this.children, function(index, child){
                    if(child.nodeName && child.nodeName.toLowerCase() === 'option'){
                        options.data.push({id: child.value, name: child.text});
                        if(child.selected){
                            options.value.push(child.value);
                        }
                    }
                });

            }

            var def = {};
            // set values from DOM container element
            $.each(this.attributes, function(i, att){
                def[att.name] = att.value;
            });
            var field = new TagSuggest(this, $.extend(options, def));
            cntr.data('tagSuggest', field);
            field.container.data('tagSuggest', field);
        });

        if(obj.size() === 1) {
            return obj.data('tagSuggest');
        }
        return obj;
    };
});