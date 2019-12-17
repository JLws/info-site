class Request(object):

    def Parameters(self, need_fields, data, miss=False):
        for field in need_fields: # find fields
            field_data = data.get(field, None)
            if field_data: # not found
                need_fields[field] = self._convert(type(need_fields[field]), field_data)

            elif miss:
                continue

            else: # found
                raise Exception('Not found ' + field)

    def _convert(self, convert_type, data):
        if convert_type == int:
            return int(data)

        else:
            return data