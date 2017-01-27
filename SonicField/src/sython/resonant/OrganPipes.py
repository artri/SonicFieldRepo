from sython.organ.Post   import \
    do_final_mix, \
    mix, \
    post_process, \
    post_process_tremolate
from sython.organ.Voices import \
    vox_humana_femail_soprano_ah,\
    vox_humana_femail_soprano_a,\
    vox_humana_femail_soprano_ma,\
    upper_accent,\
    reed,\
    string,\
    sweet_flute,\
    folk_flute,\
    shawm,\
    bright_plucked_glass,\
    plucked_glass,\
    folk_clarinet,\
    folk_basson,\
    tuned_wind,\
    orchestral_oboe,\
    cello,\
    nordic_cello, \
    upper_accent, \
    pure_triangle, \
    pure_sine, \
    simple_bell, \
    distant_wind, \
    make_addtive_resonance, \
    oboe_filter, \
    violin_filter

def sing(midi_in,beat,temperament,velocity):
    l=200.0
    midi1=Midi.long_as(midi_in,beat,l)
    midi1=Midi.legato(midi1,beat,64)
    midi2=Midi.shorter_than(midi_in,beat,l)
    midi2=Midi.legato(midi2,beat,32)
    print len(midi1),len(midi2)
    notes1 = Player.play(midi1,beat,temperament,voice=vox_humana_femail_soprano_ah, bend=True,mellow=True,velocity_correct=velocity*1.0,flat_env=False, quick_factor=1.0,pan=0.2)
    notes2 = Player.play(midi2,beat,temperament,voice=vox_humana_femail_soprano_ma, bend=True,mellow=True,velocity_correct=velocity*1.0,flat_env=False, quick_factor=1.5,pan=0.8)
    left1,right1 = post_process(notes1)
    left2,right2 = post_process(notes2)
    return mix(left1,left2),mix(right1,right2)

def strange_sing(midi_in,beat,temperament,velocity):
    midi=Midi.delay(midi_in,beat,256)
    notes1=Player.play(
        midi,
        beat,
        temperament,
        voice=vox_humana_femail_soprano_ah,
        bend=False,
        mellow=False,
        velocity_correct=velocity*1.0,
        flat_env=False,
        quick_factor=2.0,
        pan=0.5
    )
    left1,right1 = post_process(notes1)
    sf.WriteFile32((+left1,+right1),"temp/sung.wav")
    notes2=Player.play(
        midi_in,
        beat,
        temperament,
        voice=tuned_wind,
        bend=False,
        mellow=True,
        velocity_correct=velocity*0.15,
        flat_env=True,
        quick_factor=0.5,
        pitch_shift=0.25,
        pan=0.8
    )
    left2,right2 = post_process(notes2)
    sf.WriteFile32((+left2,+right2),"temp/flute1.wav")
    notes3=Player.play(
        midi_in,
        beat,
        temperament,
        voice=tuned_wind,
        bend=False,
        mellow=True,
        velocity_correct=velocity*0.15,
        flat_env=True,
        quick_factor=0.5,
        pitch_shift=0.5,
        pan=0.2
    )
    left3,right3 = post_process(notes3)
    sf.WriteFile32((+left3,+right3),"temp/flute2.wav")

    return mix(left1,left2,left3),mix(right1,right2,right3)

def distant(midi_in,beat,temperament,velocity):
    notes1=Player.play(
        midi_in,
        beat,
        temperament,
        voice=distant_wind,
        bend=True,
        mellow=False,
        velocity_correct=velocity*1.5,
        flat_env=True,
        quick_factor=1.5,
        pan = -1
    )
    return post_process(notes1)

def distant_bass(midi_in,beat,temperament,velocity):
    l = 512
    plr = make_addtive_resonance(qCorrect=1.0, rollOff=2.0, saturate=0.5, power=1.1)
    notes1=Player.play(
        midi_in,
        beat,
        temperament,
        voice=plr,
        bend=False,
        mellow=False,
        velocity_correct=velocity,
        flat_env=True,
        quick_factor=1.5,
        pure=True,
        pan = -1
    )
    return post_process(notes1)

def distant_string(midi_in,beat,temperament,velocity):
    l = 512
    plr = make_addtive_resonance(qCorrect=2.0, rollOff=1.5, power=1.0, post=violin_filter)
    notes1=Player.play(
        midi_in,
        beat,
        temperament,
        voice=plr,
        bend=True,
        mellow=False,
        velocity_correct=velocity*1.5,
        flat_env=True,
        quick_factor=1.0,
        pan = -1
    )
    return post_process(notes1)

def distant_oboe(midi_in,beat,temperament,velocity):
    plr = make_addtive_resonance(qCorrect=2.0, rollOff=1.5, saturate=0.1, power=1.4, post=oboe_filter)
    notes1=Player.play(
        midi_in,
        beat,
        temperament,
        voice=plr,
        bend=False,
        mellow=False,
        velocity_correct=velocity*1.5,
        flat_env=True,
        quick_factor=0.5,
        pure=True,
        pan = -1
    )
    return post_process_tremolate(notes1)

def distant_oboe2(midi_in,beat,temperament,velocity):
    midi=Midi.legato(midi_in,beat,200)
    plr = make_addtive_resonance(qCorrect=1.5, rollOff=1.5, saturate=0.1, power=1.4, post=oboe_filter)
    notes1=Player.play(
        midi,
        beat,
        temperament,
        voice=plr,
        bend=False,
        mellow=False,
        velocity_correct=velocity*1.5,
        flat_env=True,
        quick_factor=1.0,
        pure=True,
        pan = -1
    )
    return post_process(notes1)

def quick_flute(midi_in,beat,temperament,velocity):
    notes1=Player.play(midi1,beat,temperament,voice=folk_flute, bend=True,mellow=False,velocity_correct=velocity*0.5,flat_env=False, quick_factor=1.0,pan=-1)
    notes2=Player.play(midi2,beat,temperament,voice=tuned_wind, bend=True,mellow=False,velocity_correct=velocity*0.5,flat_env=False, quick_factor=1.0,pan=-1)
    left1,right1 = post_process(notes1)
    left2,right2 = post_process(notes2)
    return mix(left1,left2),mix(right1,right2)
    
def slow_flute(midi_in,beat,temperament,velocity):
    midi=Midi.delay(midi_in,beat,256)
    notes1=Player.play(
        midi,
        beat,
        temperament,
        voice=folk_flute,
        bend=False,
        mellow=False,
        velocity_correct=velocity*1.0,
        flat_env=False,
        quick_factor=2.0,
        pan=0.5
    )
    notes2=Player.play(
        midi_in,
        beat,
        temperament,
        voice=tuned_wind,
        bend=False,
        mellow=True,
        velocity_correct=velocity*0.15,
        flat_env=True,
        quick_factor=0.5,
        pitch_shift=0.25,
        pan=0.8
    )
    notes3=Player.play(
        midi_in,
        beat,
        temperament,
        voice=tuned_wind,
        bend=False,
        mellow=True,
        velocity_correct=velocity*0.15,
        flat_env=True,
        quick_factor=0.5,
        pitch_shift=0.5,
        pan=0.2
    )
    left1,right1 = post_process(notes1)
    left2,right2 = post_process(notes2)
    left3,right3 = post_process(notes3)
    return mix(left1,left2,left3),mix(right1,right2,right3)

def space_flute(midi_in,beat,temperament,velocity):
    notes1=Player.play(
        midi_in,
        beat,
        temperament,
        voice=folk_flute,
        bend=False,
        mellow=False,
        velocity_correct=velocity*0.25,
        flat_env=False,
        quick_factor=2.0,
        pan=0.5
    )
    notes2=Player.play(
        midi_in,
        beat,
        temperament,
        voice=tuned_wind,
        bend=False,
        mellow=True,
        velocity_correct=velocity*0.3,
        flat_env=True,
        quick_factor=0.5,
        pitch_shift=0.25,
        pan=0.8
    )
    notes3=Player.play(
        midi_in,
        beat,
        temperament,
        voice=tuned_wind,
        bend=False,
        mellow=True,
        velocity_correct=velocity*0.3,
        flat_env=True,
        quick_factor=0.5,
        pitch_shift=0.5,
        pan=0.2
    )
    notes4=Player.play(
        midi_in,
        beat,
        temperament,
        voice=upper_accent,
        bend=True,
        mellow=True,
        velocity_correct=velocity*0.05,
        flat_env=True,
        quick_factor=2.0,
        pitch_shift=2.0
    )
    left1,right1 = post_process(notes1)
    left2,right2 = post_process(notes2)
    left3,right3 = post_process(notes3)
    left4,right4 = post_process(notes4)
    return mix(left1,left2,left3,left4),mix(right1,right2,right3,right4)


def first_lead(midi_in,beat,temperament,velocity):
    notes1=Player.play(midi_in,beat,temperament,voice=folk_flute, bend=True,mellow=True, velocity_correct=velocity*1.0,flat_env=False, quick_factor=0.5,pan=-1)
    return post_process(notes1)

def third_lead(midi_in,beat,temperament,velocity):
    notes1=Player.play(midi_in,beat,temperament,voice=tuned_wind, bend=True,mellow=False, velocity_correct=velocity*1.0,flat_env=False, quick_factor=0.5,pan=-1)
    return post_process(notes1)

def bright_lead(midi_in,beat,temperament,velocity):
    notes1=Player.play(midi_in,beat,temperament,voice=plucked_glass, bend=True,decay=1500,mellow=False,velocity_correct=velocity*1.0,flat_env=False, quick_factor=0.5,pan=-1)
    midi=Midi.scatter(midi_in,beat,128)
    notes2=Player.play(midi,beat,temperament,voice=bright_plucked_glass, bend=True,decay=1250,mellow=False,velocity_correct=velocity*0.33,flat_env=True,quick_factor=0.5,pan=0.20,pitch_shift=4.0,pitch_add=1)
    midi=Midi.scatter(midi_in,beat,128)
    notes3=Player.play(midi,beat,temperament,voice=plucked_glass,decay=5000,bend=True,mellow=False,velocity_correct=velocity*0.2,flat_env=True,quick_factor=1.0,pan=0.80,pitch_add=-1)

    left1,right1=post_process(notes1)
    left2,right2=post_process(notes2)
    left3,right3=post_process(notes3)
    return mix(left1,left2,left3),mix(right1,right2,right3)
    
def second_lead(midi_in,beat,temperament,velocity):
    notes1=Player.play(midi_in,beat,temperament,voice=plucked_glass, bend=True,decay=1500,mellow=False,velocity_correct=velocity*1.0,flat_env=False, quick_factor=0.1,pan=-1)
    midi=Midi.scatter(midi_in,beat,128)
    notes2=Player.play(midi,beat,temperament,voice=bright_plucked_glass, bend=True,decay=1250,mellow=True,velocity_correct=velocity*0.25,flat_env=True,quick_factor=0.1,pan=0.20,pitch_shift=2.0,pitch_add=1)
    midi=Midi.scatter(midi_in,beat,128)
    notes3=Player.play(midi,beat,temperament,voice=plucked_glass,decay=5000,bend=True,mellow=True,velocity_correct=velocity*0.2,flat_env=False,quick_factor=0.5,pan=0.80,pitch_add=-1)

    left1,right1=post_process(notes1)
    left2,right2=post_process(notes2)
    left3,right3=post_process(notes3)
    return mix(left1,left2,left3),mix(right1,right2,right3)

def first_bass(midi_in,beat,temperament,velocity):
    notes1=Player.play(midi_in,beat,temperament,voice=folk_clarinet, bend=False,mellow=False, velocity_correct=velocity*1.0,flat_env=True, quick_factor=0.5,pan=0.25)
    notes2=Player.play(midi_in,beat,temperament,voice=folk_clarinet, bend=False,mellow=False, velocity_correct=velocity*1.0,flat_env=True, quick_factor=0.5,pan=0.75)

    left1,right1 = post_process_echo(notes1)
    left2,right2 = post_process_echo(notes2)
    return mix(left1,left2),mix(right1,right2)
        
def first_harmony(midi_in,beat,temperament,velocity):
    midi=Midi.scatter(midi_in,beat,32)
    notes1=Player.play(midi,beat,temperament,voice=folk_basson,bend=True,mellow=False,velocity_correct=velocity*1.0,flat_env=True, quick_factor=1.0,pan=-0.7)

    return post_process(notes1)

def space_sine(midi_in,beat,temperament,velocity):
    notes1=Player.play(midi_in,beat,temperament,voice=pure_sine,bend=False,mellow=False,velocity_correct=velocity*1.0,flat_env=False, quick_factor=1.0)
    return post_process(notes1)

def pure_glass(midi_in,beat,temperament,velocity):
    notes1=Player.play(midi_in,beat,temperament,voice=plucked_glass,bend=True,mellow=True,velocity_correct=velocity*1.0,flat_env=False, quick_factor=0.1)
    return post_process(notes1)    

def pure_bell(midi_in,beat,temperament,velocity):
    notes1=Player.play(midi_in,beat,temperament,voice=simple_bell,bend=False,mellow=True,velocity_correct=velocity*1.0,flat_env=True, quick_factor=0.0, pure=True)
    return post_process(notes1)    

def space_accented_wind(midi_in,beat,temperament,velocity):
    notes1=Player.play(midi_in,beat,temperament,voice=tuned_wind,bend=False,mellow=False,velocity_correct=velocity*0.02, flat_env=False,  quick_factor=6.0)
    notes2=Player.play(midi_in,beat,temperament,voice=sweet_flute,bend=False,mellow=True,velocity_correct=velocity*0.50, flat_env=False, quick_factor=2.0)
    notes3=Player.play(midi_in,beat,temperament,voice=pure_sine, bend=False,mellow=False,velocity_correct=velocity*0.02, flat_env=False, quick_factor=3.0, pitch_shift=8.0)
    left1,right1 = post_process(notes1)
    left2,right2 = post_process(notes2)
    left3,right3 = post_process_tremolate(notes3)
    return mix(left1,left2,left3),mix(right1,right2,right3)
    
def space_accented(midi_in,beat,temperament,velocity):
    notes1=Player.play(midi_in,beat,temperament,voice=pure_sine,bend=False,mellow=False,velocity_correct=velocity*1.0, flat_env=True, quick_factor=1.0)
    notes2=Player.play(midi_in,beat,temperament,voice=pure_sine,bend=False,mellow=False,velocity_correct=velocity*0.02, flat_env=False, quick_factor=3.0, pitch_shift=8.0)
    left1,right1 = post_process(notes1)
    left2,right2 = post_process_tremolate(notes2)
    return mix(left1,left2),mix(right1,right2)
    
def celloish(midi_in,beat,temperament,velocity):
    #midi=Midi.legato(midi_in,beat,100)
    #midi=Midi.scatter(midi,beat,16)
    #notes1=Player.play(midi,beat,temperament,voice=folk_basson,bend=False,mellow=True,velocity_correct=velocity*0.5,flat_env=True, quick_factor=1.0,pitch_shift=2.0,pitch_add=3)
    #midi=Midi.legato(midi_in,beat,200)
    #midi=Midi.scatter(midi,beat,16)
    notes2=Player.play(midi_in,beat,temperament,voice=nordic_cello,bend=True,mellow=False,velocity_correct=velocity*1.0,flat_env=False, quick_factor=1.0,pure=True,raw_bass=True)

    #left1,right1=post_process(notes1)
    #left2,right2=post_process(notes2)
    #return mix(left1,left2),mix(right1,right2)
    return post_process(notes2)
  