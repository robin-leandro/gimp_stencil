#!/usr/bin/python
from gimpfu import *

#TODO: center letters, kinda finicky with letters like G
#TODO: add a param to choose if conditionally remove letters (no need for I if we have E, P, Ns, etc etc)


PPI = 300
def stencil_letters(message):
    #pdb.gimp_message(c)
    letters = set(message.upper().replace(' ', ''))

    # we can get away with omitting a letter if others that include it are present
    # eg we can build a P from a B
    omissions = {
        'C': set('GOQ'),
        'F': set('EPR'),
        'I': set('BDEFHKLMNPR'),
        'J': set('U'), #(both ways)
        'L': set('E'),
        'N': set('M'),
        'O': set('CGQ'),
        'P': set('BR'),
        'U': set('J'), #(both ways)
        'V': set('W'), 
    }
    empty_set = set()

    for letter in omissions:
        intersection = omissions[letter].intersection(letters)
        if letter in letters and intersection != empty_set:
            letters.remove(letter)

    for i, letter in enumerate(letters):
        gimp.progress_init("Generating image {0} of {1}".format(i+1, len(letters)))
        gimp.progress_update(float(i+1)/float(len(letters)))

        image = pdb.gimp_image_new(12.5*PPI, 18.5*PPI, 1)

        background_layer = pdb.gimp_layer_new(image, 12.5*PPI, 18.5*PPI, 2, 'background', 100, NORMAL_MODE)
        pdb.gimp_palette_set_background('white')
        background_layer.fill(BACKGROUND_FILL)
        image.add_layer(background_layer, 0)

        # image should be around 18in tall
        layer = pdb.gimp_text_layer_new(image, letter, 'Gunplay', 18*PPI, 0)
        image.add_layer(layer, 0)

        print('layer height: {0}'.format(layer.height))
        print('image height: {0}'.format(image.height))
        print('\n\n\n\n')

        width_diff = image.width - layer.width
        free_space_y = 900 # give or take, lol
        layer.resize(image.width, image.height - free_space_y, width_diff/2, -free_space_y)
        layer.scale(image.width, image.height, True)
        layer.translate(width_diff/2, -free_space_y/2)
        pdb.gimp_display_new(image)



register(		
	"stencil_letters",
	"Stenciled Letters from String",
	'Takes a string, and generates a 12.5"x18.5" picture in a spliced font for use in stencils',
	"Robin Leandro",
	"Robin Leandro",
	"2024",
	"<Toolbox>/stencils/Stenciled Letters from String",
	"",
	[(PF_STRING, "message", 'message to be stenciled. One 12.5"x18.5" picture will be generated for unique each letter', 'FREE PALESTINE')],
	[],
	stencil_letters)

main()