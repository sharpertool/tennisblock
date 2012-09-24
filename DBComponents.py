__author__ = 'kutenai'

import re

from DBCategories import *

class DBComponents(DBCategories):

    def __init__(self,connection):
        super(DBComponents,self).__init__(connection)

        self.setTableNames()

    def setTableNames(self):

        self.compTable = "components"
        self.vendCompTable = "vend_components"
        self.pinTable = "component_pins"
        self.lblTable = "component_labels"
        self.compParamsTable = "component_params"
        self.catTable = "categories"
        self.modelTable = "param_models"
        self.paramTable = "parameters"

    def clearComponents(self):
        """
        Just delete all from the current tables.
        """
        curs = self.getCursor()
        curs.execute("delete from %s" % self.compTable)
        curs.execute("alter table %s AUTO_INCREMENT=1" % self.compTable)
        curs.execute("delete from %s" % self.compParamsTable)
        curs.execute("alter table %s AUTO_INCREMENT=1" % self.compParamsTable)
        curs.execute("delete from %s" % self.pinTable)
        curs.execute("alter table %s AUTO_INCREMENT=1" % self.pinTable)
        curs.execute("delete from %s" % self.lblTable)
        curs.execute("alter table %s AUTO_INCREMENT=1" % self.lblTable)

    def getInsertCategoryID(self,category):
        """
        Retrieve the id for a category.

        If the category does not exist, insert
        it.
        """

        cat_id = self.getCategoryID(category)

        if cat_id == None:
            sql = """
            insert into %s
            (
                name, display_order, category_group
            )
            values (
                "%s",
                0,
                "default"
            )
            """ % (self.catTable,category)

            curs.execute(sql)
            cat_id = self.conn.insert_id()

        return cat_id

    def getComponentPins(self,component_id):
        """
        Retrieve a list of pins for the specified component_id

        The pins are returned as a list of dictionaries.
        """
        curs = self.getCursor()

        curs.execute("""

        select
            pin_id,
            label,
            electrical_type,
            pin_number,
            symbol_pin_number,
            pin_net
        from
            %s
        where
            component_id = %d
        order by pin_number
                     """ % (self.pinTable,component_id) )

        pins = curs.fetchallDict()

        return pins

    def getComponentLabels(self,component_id):
        """
        Retrieve a list of labels for the specified component_id

        The labels are returned as a list of dictionaries.
        """
        curs = self.getCursor()

        curs.execute("""

        select
            label_id,
            label_name,
            default_value,
            label_type,
            position_x,
            position_y,
            position_name,
            anchor_point,
            line_number
        from
            %s
        where
            component_id = %d
                     """ % (self.lblTable, component_id) )

        pins = curs.fetchallDict()

        return pins

    def getComponentParams(self,component_id):
        """
        Retrieve a list of parameters for the specified component_id

        """
        curs = self.getCursor()

        curs.execute("""

        select
            name,
            value,
            visible,
            editable
        from
            %s
        where
            component_id = %d
                     """ % (self.compParamsTable,component_id) )

        params = curs.fetchallDict()

        return params

    def getComponentsForCategory(self,category,parent_id=None):
        """
        Retrieve a list of components that match the specified category.

        The components are returned as a list of dictionaries.
        """

        curs = self.getCursor()

        if parent_id:
            sql = """

            select
                CATS.name category,
                CATS.parent_id,
                component_id,
                CO.name, description,
                ref_prefix,
                bom_include,
                CO.display_order,
                symbol_id,
                preview_symbol_id,
                spice_id,
                spice_model,
                persistent_id,
                version,
                spice_type,
                paramsets,
                search_keys,
                search_params
            from
                %s CO,%s CATS
            where
                CO.category_id = CATS.category_id
                and CATS.name = "%s"
                and CATS.parent_id = %d
            order by display_order
                """ % (self.compTable,self.catTable, category,parent_id)

        else:

            sql = """

            select
                CATS.name category,
                component_id,
                CO.name, description,
                ref_prefix,
                bom_include,
                CO.display_order,
                symbol_id,
                preview_symbol_id,
                spice_id,
                spice_model,
                persistent_id,
                version,
                paramsets,
                search_keys,
                search_params

            from
                %s CO,%s CATS
            where
                CO.category_id = CATS.category_id
                and CATS.name = "%s"
            order by display_order
                """ % (self.compTable,self.catTable,category)

        curs.execute(sql)

        components = curs.fetchallDict()
        return components

    def insertSubCategory(self,parent,subcategory):

        pname = re.sub("\s+","_",parent)
        catname = re.sub("\s+","_",subcategory)

        super(DBComponents,self).updateSubCategory(pname,catname)

        cat_id = self.getSubCategoryID(parent,catname)
        if cat_id == None:
            # Insert the category..don't know the parent, so
            # just make this a parent of 0

            # Remove any spaces for the name. Display name
            # is the one passed in here.
            dispOrder = 0 # No way to set this differently
            cat_id = self.insertCategory(0,catname,category,dispOrder)



    def insertComponent(self,curs,parentcat,category,order,component,pins):
        """"
        Insert the component specified in the component dict.

        The dictionary should contain all of the required fields
        as indicated in the parse code.
        """

        nm = component['name']
        desc = component['description']
        ref = component['ref_prefix']
        pid = component['persistent_id']
        version = component['version']
        if component.has_key('SymbolID'):
            sym_id = component['SymbolID']
        else:
            sym_id = ""

        if component.has_key('spiceModel'):
            spice_model = component['spiceModel']
        else:
            spice_model = ""

        if component.has_key('PreviewID'):
            prev_id = component['PreviewID']
        else:
            prev_id = sym_id

        if component.has_key('paramsets'):
            paramsets = component['paramsets']
        else:
            paramsets = ""

        cat_id = self.getSubCategoryIDWithInsert(parentcat,category)

        if component['bom_include']:
            bom = 1
        else:
            bom = 0

        spice_id = 0

        if component.has_key('spicetype'):
            spice_type = component['spicetype']
        else:
            spice_type = ""

        skeys = ""
        sparams = ""
        if component.has_key('SearchKeys'):
            skeys = component['SearchKeys']
        if component.has_key('SearchParams'):
            sparams = component['SearchParams']

        sql = ("""
            insert into %s
            (   name,
                description,
                ref_prefix,
                bom_include,
                display_order,
                symbol_id,
                preview_symbol_id,
                spice_id,
                spice_type,
                category_id,
                spice_model,
                persistent_id,
                version,
                paramsets,
                search_keys,
                search_params
            )

            values (
                "%s",
                "%s",
                "%s",
                %d,
                %d,
                "%s",
                "%s",
                %d,
                "%s",
                %d,
                "%s",
                "%s",
                "%s",
                "%s",
                "%s","%s"
            )
            """ % (self.compTable, nm,desc,ref,bom,order,
                   sym_id,prev_id,spice_id,spice_type,
                   cat_id,spice_model,pid,version,paramsets,skeys,sparams))

        curs.execute(sql)
        comp_id = self.insertId()
        print "Inserted %s:%s #%d" % (category, nm, order)

        self.insertCompPins(curs,comp_id,pins)

        # Insert any labels
        for lblDict in component['labels']:
            self.insertLabel(curs,comp_id,lblDict)

        return comp_id

    def insertCompPins(self,curs,comp_id,pins):
        pin_num = 1
        for pin in pins:
            if pin.has_key('id'):
                lbl = pin['id']
            else:
                lbl = str(pin_num)

            if pin.has_key('net'):
                pinNet = pin['net']
            else:
                pinNet = ""

            self.insertPin(curs,comp_id,
                lbl,
                "passive", # Electrical type default
                pin_num,
                pin_num, # Symbol Pin Number default
                pinNet
            )

            pin_num = pin_num + 1

    def insertPin(self,curs,id,lbl,
                  elect_type, pinNum, symbolPinNum, pinNet):
        """
        Insert a pin for the component id specified.
        """

        sql = """
            insert into %s
            (   component_id,
                label,
                electrical_type,
                pin_number,
                symbol_pin_number,
                pin_net
            )

            values (
            %d,
            "%s",
            "%s",
            %d,
            %d,
            "%s"
            )
            """ % (self.pinTable, id,lbl,elect_type,pinNum, symbolPinNum,pinNet)

        curs.execute(sql)

    def insertComponentParams(self,curs,comp_id,paramList):

        for param in paramList:

            if param.has_key('edit'):
                edit = param['edit']
            else:
                edit = "1"

            if param.has_key('show'):
                show = param['show']
            else:
                show = "1"

            sql = """
                insert into %s
                (
                    component_id,
                    name,
                    value,
                    visible,
                    editable
                )

                values (
                    %d,
                    "%s",
                    "%s",
                    "%s",
                    "%s"
                )
                """ % (
                    self.compParamsTable,
                    comp_id,
                    param['name'],
                    param['value'],
                    show,
                    edit
                )

            curs.execute(sql)

    def insertLabel(self,curs,id,label):

        """
        Insert a label for the component id specified.
        """
        name    = label['name']
        value   = label['value']
        pos     = label['pos']

        position = pos[0]
        anchor = pos[1]
        line = pos[2]
        posx = 0
        posy = 0

        cols = "position_name"
        vals = '"%s"' % position

        if anchor:
            cols += ',anchor_point'
            vals += ',"%s"' % anchor

        if line:
            cols += ',line_number'
            vals += ',%s' % line

        if value:
            cols += ',default_value'
            vals += ',"%s"' % value

        sql = """
            insert into %s
            (
                component_id,
                label_name,
                label_type,
                position_x,
                position_y,
                %s
            )

            values (
                %d,
                "%s",
                "%s",
                0, 0,
                %s
            )
            """ % (self.lblTable, cols,id,name,value,vals)

        try:
            curs.execute(sql)
        except Exception as e:
            print ("Failed with sql:%s" % sql)

    def clearParamSets(self):

        curs = self.getCursor()

        curs.execute("delete from %s" % self.paramTable)
        curs.execute("alter table %s AUTO_INCREMENT=1" % self.paramTable)

        curs.execute("delete from %s" % self.modelTable)
        curs.execute("alter table %s AUTO_INCREMENT=1" % self.modelTable)

    def insertParam(self,set_name,param):

        param_order = 0
        if param.has_key('order'):
            try:
                param_order = int(param['order'])
            except:
                pass

        sql = """
        insert into %s
        (
             paramset_name,
             name,
             disp_name,
             param_order,
             fldtype,
             default_val,
             rule,
             units,
             visibility,
             tip
        )

        values (
            "%s","%s","%s",%d,"%s","%s","%s","%s","%s","%s"
        )
        """ % (self.paramTable,
               set_name,
               param['id'],
               param['display'],
               param_order,
               param['type'],
               param['default'],
               param['rule'],
               param['units'],
               param['visibility'],
               param['tip']
            )

        curs = self.getCursor()
        curs.execute(sql)
        param_id = self.insertId()

        if param['type'] == 'list' and param.has_key('listdata'):
            models = param['listdata']
            if len(models) > 0:
                self.insertParamModels(param_id,models)

        return param_id

    def insertParamModels(self,param_id,models):

        curs = self.getCursor()
        for model in models:

            sql = """
            insert into %s
            (
                 param_id,
                 vendor,
                 model,
                 description
            )

            values (
                %d,"%s","%s","%s"
            )
            """ % (self.modelTable,
                   param_id,
                   model['vendor'],
                   model['model'],
                   model['desc']
                )

            curs.execute(sql)

    def queryParamSets(self):
        """
        Query all parameter sets, including any model lists associated with a
        param set.
        """
        curs = self.getCursor()

        curs.execute("""

        select
            paramset_name,
            param_id,
            name,
            disp_name,
            param_order,
            fldtype,
            default_val,
            rule,
            units,
            visibility,
            tip
        from
            %s
        order by
            paramset_name,param_order
                     """ % self.paramTable)

        params = curs.fetchallDict()

        return params

    def queryParamSetList(self,param_id):
        """
        Query all list parameters for the given param_id
        """
        curs = self.getCursor()

        curs.execute("""

        select
            model_id,
            vendor,
            model,
            description
        from
            %s
        where
            param_id = %d
                     """ % (self.modelTable,param_id))

        paramList = curs.fetchallDict()

        return paramList

    def queryUsedSymbols(self):
        """
        Query all list parameters for the given param_id
        """
        curs = self.getCursor()

        sql = """
            SELECT distinct(symbol_id)
            from (
                select symbol_id from %s
                union
                select preview_symbol_id from %s
                union
                select symbol_id from %s
                union
                select preview_symbol_id from %s
            ) a
            order by symbol_id
        """ % (self.compTable,self.compTable,self.vendCompTable,self.vendCompTable)

        #sql = "select symbol_id,preview_symbol_id from %s" % self.compTable
        curs.execute(sql)

        comps = curs.fetchallDict()

        return comps

def main():

    # Left over.. could put some test code here.
    pass


if __name__ == '__main__':
    main()
