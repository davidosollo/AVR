def findDecision(obj): #obj[0]: experiencia, obj[1]: disciplina, obj[2]: empatia, obj[3]: liderazgo, obj[4]: seguridad, obj[5]: habilidad_tecnologica, obj[6]: habilidad_pedagogica, obj[7]: vocacion, obj[8]: relaciones_inter, obj[9]: curiosidad, obj[10]: paciencia, obj[11]: normal_D, obj[12]: normal_I, obj[13]: normal_S, obj[14]: normal_C, obj[15]: motivacion_D, obj[16]: motivacion_I, obj[17]: motivacion_S, obj[18]: motivacion_C, obj[19]: presion_D, obj[20]: presion_I, obj[21]: presion_S, obj[22]: presion_C
   # {"feature": "motivacion_I", "instances": 700, "metric_value": 0.3387, "depth": 1}
   if obj[16]>15:
      # {"feature": "presion_S", "instances": 596, "metric_value": 0.2807, "depth": 2}
      if obj[21]>1:
         # {"feature": "presion_D", "instances": 591, "metric_value": 0.2751, "depth": 3}
         if obj[19]<=49.90186125211506:
            # {"feature": "motivacion_D", "instances": 304, "metric_value": 0.121, "depth": 4}
            if obj[15]<=73.23532465316393:
               # {"feature": "presion_C", "instances": 231, "metric_value": 0.0718, "depth": 5}
               if obj[22]<=73.96194298207432:
                  return 'No'
               elif obj[22]>73.96194298207432:
                  # {"feature": "normal_I", "instances": 58, "metric_value": 0.2164, "depth": 6}
                  if obj[12]>30:
                     return 'No'
                  elif obj[12]<=30:
                     # {"feature": "motivacion_C", "instances": 19, "metric_value": 0.4855, "depth": 7}
                     if obj[18]>15:
                        # {"feature": "seguridad", "instances": 18, "metric_value": 0.3095, "depth": 8}
                        if obj[4] == 'alto':
                           return 'No'
                        elif obj[4] == 'bajo':
                           return 'No'
                        elif obj[4] == 'medio_bajo':
                           return 'No'
                        elif obj[4] == 'medio_alto':
                           return 'No'
                        elif obj[4] == 'medio':
                           # {"feature": "experiencia", "instances": 2, "metric_value": 1.0, "depth": 9}
                           if obj[0] == 'medio':
                              return 'No'
                           elif obj[0] == 'medio_alto':
                              return 'Yes'
                           else:
                              return 'Yes'
                        else:
                           return 'No'
                     elif obj[18]<=15:
                        return 'Yes'
                     else:
                        return 'Yes'
                  else:
                     return 'No'
               else:
                  return 'No'
            elif obj[15]>73.23532465316393:
               # {"feature": "normal_I", "instances": 73, "metric_value": 0.2473, "depth": 5}
               if obj[12]>48.97260273972603:
                  # {"feature": "presion_C", "instances": 38, "metric_value": 0.3985, "depth": 6}
                  if obj[22]>28.502379448923524:
                     # {"feature": "normal_D", "instances": 29, "metric_value": 0.2164, "depth": 7}
                     if obj[11]>30:
                        return 'No'
                     elif obj[11]<=30:
                        # {"feature": "normal_C", "instances": 7, "metric_value": 0.5917, "depth": 8}
                        if obj[14]>30:
                           return 'No'
                        elif obj[14]<=30:
                           # {"feature": "experiencia", "instances": 2, "metric_value": 1.0, "depth": 9}
                           if obj[0] == 'medio_bajo':
                              return 'Yes'
                           elif obj[0] == 'medio_alto':
                              return 'No'
                           else:
                              return 'No'
                        else:
                           return 'No'
                     else:
                        return 'No'
                  elif obj[22]<=28.502379448923524:
                     # {"feature": "motivacion_C", "instances": 9, "metric_value": 0.7642, "depth": 7}
                     if obj[18]<=44:
                        return 'No'
                     elif obj[18]>44:
                        # {"feature": "seguridad", "instances": 3, "metric_value": 0.9183, "depth": 8}
                        if obj[4] == 'medio_alto':
                           return 'Yes'
                        elif obj[4] == 'bajo':
                           return 'No'
                        else:
                           return 'No'
                     else:
                        return 'Yes'
                  else:
                     return 'No'
               elif obj[12]<=48.97260273972603:
                  return 'No'
               else:
                  return 'No'
            else:
               return 'No'
         elif obj[19]>49.90186125211506:
            # {"feature": "habilidad_tecnologica", "instances": 287, "metric_value": 0.4027, "depth": 4}
            if obj[5] == 'medio_bajo':
               # {"feature": "motivacion_C", "instances": 67, "metric_value": 0.6442, "depth": 5}
               if obj[18]>24.267665495273175:
                  # {"feature": "paciencia", "instances": 51, "metric_value": 0.5226, "depth": 6}
                  if obj[10] == 'alto':
                     # {"feature": "vocacion", "instances": 14, "metric_value": 0.8631, "depth": 7}
                     if obj[7] == 'medio_alto':
                        return 'No'
                     elif obj[7] == 'bajo':
                        # {"feature": "normal_D", "instances": 4, "metric_value": 0.8113, "depth": 8}
                        if obj[11]>30:
                           return 'No'
                        elif obj[11]<=30:
                           return 'Yes'
                        else:
                           return 'Yes'
                     elif obj[7] == 'medio':
                        return 'No'
                     elif obj[7] == 'medio_bajo':
                        return 'Yes'
                     elif obj[7] == 'alto':
                        return 'Yes'
                     else:
                        return 'Yes'
                  elif obj[10] == 'medio_alto':
                     return 'No'
                  elif obj[10] == 'medio':
                     # {"feature": "motivacion_S", "instances": 9, "metric_value": 0.7642, "depth": 7}
                     if obj[17]>32:
                        return 'No'
                     elif obj[17]<=32:
                        # {"feature": "habilidad_pedagogica", "instances": 3, "metric_value": 0.9183, "depth": 8}
                        if obj[6] == 'medio':
                           return 'Yes'
                        elif obj[6] == 'medio_bajo':
                           return 'No'
                        else:
                           return 'No'
                     else:
                        return 'Yes'
                  elif obj[10] == 'medio_bajo':
                     return 'No'
                  elif obj[10] == 'bajo':
                     return 'No'
                  else:
                     return 'No'
               elif obj[18]<=24.267665495273175:
                  # {"feature": "motivacion_D", "instances": 16, "metric_value": 0.896, "depth": 6}
                  if obj[15]<=58:
                     # {"feature": "liderazgo", "instances": 11, "metric_value": 0.4395, "depth": 7}
                     if obj[3] == 'medio_alto':
                        return 'No'
                     elif obj[3] == 'medio_bajo':
                        return 'No'
                     elif obj[3] == 'alto':
                        return 'Yes'
                     else:
                        return 'Yes'
                  elif obj[15]>58:
                     # {"feature": "presion_I", "instances": 5, "metric_value": 0.7219, "depth": 7}
                     if obj[20]<=69:
                        return 'Yes'
                     elif obj[20]>69:
                        return 'No'
                     else:
                        return 'No'
                  else:
                     return 'Yes'
               else:
                  return 'No'
            elif obj[5] == 'medio':
               # {"feature": "normal_C", "instances": 62, "metric_value": 0.4587, "depth": 5}
               if obj[14]<=68.03613507836369:
                  # {"feature": "presion_I", "instances": 43, "metric_value": 0.583, "depth": 6}
                  if obj[20]>25.111975860594104:
                     # {"feature": "presion_C", "instances": 33, "metric_value": 0.684, "depth": 7}
                     if obj[22]<=59:
                        # {"feature": "experiencia", "instances": 23, "metric_value": 0.8281, "depth": 8}
                        if obj[0] == 'medio_alto':
                           # {"feature": "motivacion_D", "instances": 6, "metric_value": 0.9183, "depth": 9}
                           if obj[15]>37:
                              return 'No'
                           elif obj[15]<=37:
                              return 'Yes'
                           else:
                              return 'Yes'
                        elif obj[0] == 'medio':
                           # {"feature": "motivacion_D", "instances": 6, "metric_value": 0.9183, "depth": 9}
                           if obj[15]>51:
                              return 'Yes'
                           elif obj[15]<=51:
                              return 'No'
                           else:
                              return 'No'
                        elif obj[0] == 'medio_bajo':
                           return 'No'
                        elif obj[0] == 'alto':
                           return 'No'
                        elif obj[0] == 'bajo':
                           return 'No'
                        else:
                           return 'No'
                     elif obj[22]>59:
                        return 'No'
                     else:
                        return 'No'
                  elif obj[20]<=25.111975860594104:
                     return 'No'
                  else:
                     return 'No'
               elif obj[14]>68.03613507836369:
                  return 'No'
               else:
                  return 'No'
            elif obj[5] == 'alto':
               # {"feature": "presion_C", "instances": 57, "metric_value": 0.1274, "depth": 5}
               if obj[22]>15:
                  return 'No'
               elif obj[22]<=15:
                  # {"feature": "motivacion_D", "instances": 8, "metric_value": 0.5436, "depth": 6}
                  if obj[15]>31:
                     return 'No'
                  elif obj[15]<=31:
                     return 'Yes'
                  else:
                     return 'Yes'
               else:
                  return 'No'
            elif obj[5] == 'medio_alto':
               # {"feature": "presion_C", "instances": 52, "metric_value": 0.3912, "depth": 5}
               if obj[22]<=54.57692307692308:
                  # {"feature": "habilidad_pedagogica", "instances": 26, "metric_value": 0.6194, "depth": 6}
                  if obj[6] == 'medio':
                     # {"feature": "disciplina", "instances": 8, "metric_value": 1.0, "depth": 7}
                     if obj[1] == 'medio_alto':
                        return 'Yes'
                     elif obj[1] == 'medio':
                        # {"feature": "experiencia", "instances": 2, "metric_value": 1.0, "depth": 8}
                        if obj[0] == 'alto':
                           return 'Yes'
                        elif obj[0] == 'medio_alto':
                           return 'No'
                        else:
                           return 'No'
                     elif obj[1] == 'alto':
                        return 'No'
                     elif obj[1] == 'bajo':
                        return 'No'
                     else:
                        return 'No'
                  elif obj[6] == 'medio_bajo':
                     return 'No'
                  elif obj[6] == 'alto':
                     return 'No'
                  elif obj[6] == 'medio_alto':
                     return 'No'
                  elif obj[6] == 'bajo':
                     return 'No'
                  else:
                     return 'No'
               elif obj[22]>54.57692307692308:
                  return 'No'
               else:
                  return 'No'
            elif obj[5] == 'bajo':
               # {"feature": "normal_S", "instances": 49, "metric_value": 0.1437, "depth": 5}
               if obj[13]<=69:
                  return 'No'
               elif obj[13]>69:
                  # {"feature": "normal_I", "instances": 12, "metric_value": 0.4138, "depth": 6}
                  if obj[12]>33:
                     return 'No'
                  elif obj[12]<=33:
                     # {"feature": "experiencia", "instances": 2, "metric_value": 1.0, "depth": 7}
                     if obj[0] == 'alto':
                        return 'No'
                     elif obj[0] == 'bajo':
                        return 'Yes'
                     else:
                        return 'Yes'
                  else:
                     return 'No'
               else:
                  return 'No'
            else:
               return 'No'
         else:
            return 'No'
      elif obj[21]<=1:
         # {"feature": "normal_D", "instances": 5, "metric_value": 0.7219, "depth": 3}
         if obj[11]>30:
            return 'No'
         elif obj[11]<=30:
            return 'Yes'
         else:
            return 'Yes'
      else:
         return 'No'
   elif obj[16]<=15:
      # {"feature": "presion_S", "instances": 104, "metric_value": 0.5952, "depth": 2}
      if obj[21]>20.744702094796615:
         # {"feature": "relaciones_inter", "instances": 85, "metric_value": 0.6723, "depth": 3}
         if obj[8] == 'alto':
            # {"feature": "presion_C", "instances": 20, "metric_value": 0.7219, "depth": 4}
            if obj[22]>54:
               return 'No'
            elif obj[22]<=54:
               # {"feature": "normal_I", "instances": 10, "metric_value": 0.971, "depth": 5}
               if obj[12]<=65:
                  # {"feature": "motivacion_D", "instances": 8, "metric_value": 0.8113, "depth": 6}
                  if obj[15]<=84:
                     # {"feature": "curiosidad", "instances": 7, "metric_value": 0.5917, "depth": 7}
                     if obj[9] == 'alto':
                        return 'No'
                     elif obj[9] == 'medio_bajo':
                        return 'No'
                     elif obj[9] == 'medio_alto':
                        return 'Yes'
                     elif obj[9] == 'medio':
                        return 'No'
                     else:
                        return 'No'
                  elif obj[15]>84:
                     return 'Yes'
                  else:
                     return 'Yes'
               elif obj[12]>65:
                  return 'Yes'
               else:
                  return 'Yes'
            else:
               return 'No'
         elif obj[8] == 'bajo':
            # {"feature": "normal_C", "instances": 18, "metric_value": 0.7642, "depth": 4}
            if obj[14]<=69:
               # {"feature": "motivacion_D", "instances": 17, "metric_value": 0.6723, "depth": 5}
               if obj[15]<=52:
                  return 'No'
               elif obj[15]>52:
                  # {"feature": "normal_I", "instances": 6, "metric_value": 1.0, "depth": 6}
                  if obj[12]>30:
                     # {"feature": "normal_S", "instances": 4, "metric_value": 0.8113, "depth": 7}
                     if obj[13]>39:
                        return 'No'
                     elif obj[13]<=39:
                        return 'Yes'
                     else:
                        return 'Yes'
                  elif obj[12]<=30:
                     return 'Yes'
                  else:
                     return 'Yes'
               else:
                  return 'No'
            elif obj[14]>69:
               return 'Yes'
            else:
               return 'Yes'
         elif obj[8] == 'medio_bajo':
            return 'No'
         elif obj[8] == 'medio':
            # {"feature": "motivacion_D", "instances": 15, "metric_value": 0.971, "depth": 4}
            if obj[15]>49:
               # {"feature": "motivacion_S", "instances": 11, "metric_value": 0.994, "depth": 5}
               if obj[17]<=84:
                  # {"feature": "normal_C", "instances": 9, "metric_value": 0.9183, "depth": 6}
                  if obj[14]<=61:
                     return 'Yes'
                  elif obj[14]>61:
                     # {"feature": "presion_C", "instances": 4, "metric_value": 0.8113, "depth": 7}
                     if obj[22]>15:
                        return 'No'
                     elif obj[22]<=15:
                        return 'Yes'
                     else:
                        return 'Yes'
                  else:
                     return 'No'
               elif obj[17]>84:
                  return 'No'
               else:
                  return 'No'
            elif obj[15]<=49:
               return 'No'
            else:
               return 'No'
         elif obj[8] == 'medio_alto':
            # {"feature": "presion_I", "instances": 15, "metric_value": 0.3534, "depth": 4}
            if obj[20]>18:
               return 'No'
            elif obj[20]<=18:
               # {"feature": "experiencia", "instances": 2, "metric_value": 1.0, "depth": 5}
               if obj[0] == 'medio_bajo':
                  return 'No'
               elif obj[0] == 'medio':
                  return 'Yes'
               else:
                  return 'Yes'
            else:
               return 'No'
         else:
            return 'No'
      elif obj[21]<=20.744702094796615:
         return 'No'
      else:
         return 'No'
   else:
      return 'No'
